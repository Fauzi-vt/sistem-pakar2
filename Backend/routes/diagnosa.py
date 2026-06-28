"""
diagnosa.py - Teorema Bayes Diagnosis Engine for Sistem Pakar THT
================================================================

Database Schema Reference:
  penyakit         : id (int), kode_penyakit, nama_penyakit, deskripsi, solusi,
                     prior_probability P(H) (float), created_at
  gejala           : id (int), kode_gejala, nama_gejala, created_at
  aturan           : id, penyakit_id (int), gejala_id (int),
                     conditional_probability P(Ei|H) (float), created_at
  riwayat_diagnosa : id, user_id (uuid|null), gejala_terpilih (json),
                     hasil_diagnosa (json), created_at

Algoritma Teorema Bayes (Bayes' Theorem) - multi-evidence:

  Formula:
    P(H|E₁, E₂, ..., Eₙ) = P(H) × ∏ P(Eᵢ|H) / P(E)

  Keterangan:
    P(H)     = prior_probability penyakit H (kolom `prior_probability` di tabel penyakit).
               Jika belum diset (NULL atau 0), gunakan prior seragam = 1 / total_penyakit.
    P(Eᵢ|H) = conditional_probability gejala Eᵢ diberikan penyakit H
               (kolom `conditional_probability` di tabel aturan, nilai pakar 0.0–1.0).
               Hanya gejala yang dipilih pasien AND memiliki aturan untuk H yang dihitung.
    P(E)     = faktor normalisasi = Σₖ [ P(Hₖ) × ∏ P(Eᵢ|Hₖ) ] untuk semua kandidat penyakit.
    P(H|E)   = probabilitas posterior — nilai yang ditampilkan sebagai persentase keyakinan.

  Asumsi: independence antara gejala diberikan penyakit (conditional independence).

Status mapping (berdasarkan nilai posterior P(H|E) 0.0-1.0):
  <= 0.2 -> "Tidak Ada"
  <= 0.4 -> "Mungkin"
  <= 0.6 -> "Kemungkinan Besar"
  <  0.8 -> "Hampir Pasti"
  >= 0.8 -> "Pasti"

Endpoint:
  POST /api/diagnosa  - run Teorema Bayes and return sorted results
"""

import os
import json
import logging
from typing import Optional, List

from fastapi import APIRouter, HTTPException, Depends, status as http_status
from dependencies import get_current_user, require_role, UserModel
from pydantic import BaseModel, Field
from supabase import create_client, Client
from dotenv import load_dotenv

# -- Logging -------------------------------------------------------------------
logger = logging.getLogger(__name__)

# -- Supabase Client -----------------------------------------------------------
load_dotenv()
_SUPABASE_URL = os.getenv("SUPABASE_URL", "")
_SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")
supabase: Client = create_client(_SUPABASE_URL, _SUPABASE_KEY)

# -- Router --------------------------------------------------------------------
router = APIRouter(
    prefix="/api/diagnosa",
    tags=["Diagnosa"],
)


# =============================================================================
# PYDANTIC SCHEMAS
# =============================================================================

class DiagnosaRequest(BaseModel):
    """Payload sent by the frontend to trigger a Teorema Bayes diagnosis."""

    user_id: Optional[str] = Field(
        default=None,
        description="UUID of the logged-in user (optional for guest sessions).",
    )
    gejala_ids: List[int] = Field(
        ...,
        min_length=1,
        description="List of gejala IDs selected by the patient (must not be empty).",
        examples=[[1, 3, 7]],
    )


class CalculationDetail(BaseModel):
    """
    Rincian langkah-langkah perhitungan Teorema Bayes untuk satu penyakit.

    Rumus: P(H|E₁,...,Eₙ) = [P(H) × ∏ P(Eᵢ|H)] / P(E)
    """

    nilai_gejala: List[float]       # P(Eᵢ|H): conditional probability tiap gejala yang cocok
    prior: float                    # P(H): prior probability penyakit
    likelihood_product: float       # ∏ P(Eᵢ|H): hasil kali semua conditional probability
    unnormalized_posterior: float   # P(H) × ∏ P(Eᵢ|H): skor sebelum normalisasi
    normalization_constant: float   # P(E): faktor normalisasi = Σ unnormalized semua kandidat
    posterior: float                # P(H|E): probabilitas posterior final (0.0 – 1.0)


class PenyakitHasil(BaseModel):
    """A single disease result entry returned after the Bayes calculation."""

    penyakit_id: int
    kode_penyakit: str
    nama_penyakit: str
    deskripsi: Optional[str] = None
    solusi: Optional[str] = None
    persentase: float           # posterior × 100, dibulatkan 4 desimal
    status: str                 # interpretasi verbal dari nilai posterior
    gejala_cocok: List[int]     # gejala_ids yang cocok dengan aturan penyakit ini
    detail: CalculationDetail   # rincian langkah perhitungan Teorema Bayes


class DiagnosaResponse(BaseModel):
    """Full response envelope returned by POST /api/diagnosa."""

    success: bool = True
    message: str
    riwayat_id: Optional[int] = None   # ID of the saved history record (if any)
    total_gejala_dipilih: int
    hasil: List[PenyakitHasil]          # sorted descending by persentase


# =============================================================================
# HELPERS
# =============================================================================

def _get_status(posterior: float) -> str:
    """
    Petakan nilai posterior P(H|E) (0.0–1.0) ke label verbal diagnosis.

      <= 0.2  ->  "Tidak Ada"
      <= 0.4  ->  "Mungkin"
      <= 0.6  ->  "Kemungkinan Besar"
      <  0.8  ->  "Hampir Pasti"
      >= 0.8  ->  "Pasti"
    """
    if posterior <= 0.2:
        return "Tidak Ada"
    if posterior <= 0.4:
        return "Mungkin"
    if posterior <= 0.6:
        return "Kemungkinan Besar"
    if posterior < 0.8:
        return "Hampir Pasti"
    return "Pasti"


def _fetch_all_penyakit() -> list[dict]:
    """Return every disease record from the penyakit table."""
    try:
        response = (
            supabase
            .table("penyakit")
            .select("id, kode_penyakit, nama_penyakit, deskripsi, solusi, prior_probability")
            .execute()
        )
        return response.data or []
    except Exception as exc:
        logger.error("Failed to fetch penyakit: %s", exc)
        raise


def _fetch_aturan_for_gejala(gejala_ids: list[int]) -> list[dict]:
    """
    Return all rules whose gejala_id is in the selected list.
    Each row: { penyakit_id, gejala_id, conditional_probability P(Ei|H) }
    """
    try:
        response = (
            supabase
            .table("aturan")
            .select("penyakit_id, gejala_id, conditional_probability")
            .in_("gejala_id", gejala_ids)
            .execute()
        )
        return response.data or []
    except Exception as exc:
        logger.error("Failed to fetch aturan: %s", exc)
        raise


def _save_riwayat(
    user_id: Optional[str],
    gejala_ids: List[int],
    hasil: List[PenyakitHasil],
) -> Optional[int]:
    """
    Persist the diagnosis session to riwayat_diagnosa.
    Returns the new row ID, or None if saving failed (non-fatal).

    - gejala_terpilih : JSON array of selected gejala IDs
    - hasil_diagnosa  : JSON array with penyakit name, percentage, and status
    """
    payload: dict = {
        "gejala_terpilih": json.dumps(gejala_ids),
        "hasil_diagnosa": json.dumps(
            [
                {
                    "penyakit_id":   h.penyakit_id,
                    "kode_penyakit": h.kode_penyakit,
                    "nama_penyakit": h.nama_penyakit,
                    "persentase":    h.persentase,
                    "status":        h.status,
                }
                for h in hasil
            ]
        ),
    }
    if user_id:
        payload["user_id"] = user_id

    try:
        res = supabase.table("riwayat_diagnosa").insert(payload).execute()
        if res.data:
            return res.data[0].get("id")
    except Exception as exc:
        # History saving is non-fatal - log and continue
        logger.warning("Failed to save riwayat_diagnosa: %s", exc)

    return None


# =============================================================================
# CORE - Teorema Bayes calculation
# =============================================================================

def _run_teorema_bayes(
    penyakit_list: list[dict],
    aturan_list: list[dict],
    gejala_ids: List[int],
) -> List[PenyakitHasil]:
    """
    Implementasi Teorema Bayes (Bayes' Theorem) untuk multi-evidence diagnosis.

    Formula:
      P(H|E₁, E₂, ..., Eₙ) = [P(H) × ∏ P(Eᵢ|H)] / P(E)

    Langkah-langkah:
      1. Ambil P(H) dari kolom `prior_probability` tabel penyakit.
         Jika NULL atau 0, gunakan prior seragam = 1 / total_penyakit.
      2. Untuk setiap penyakit H:
         a. Filter gejala yang dipilih pasien DAN memiliki aturan untuk H
            → nilai_gejala = [P(Eᵢ|H) untuk setiap gejala yang cocok]
         b. Hitung likelihood product: ∏ P(Eᵢ|H)
         c. Hitung unnormalized posterior: P(H) × ∏ P(Eᵢ|H)
      3. Faktor normalisasi P(E) = Σ semua unnormalized_posterior kandidat
      4. Posterior final: P(H|E) = unnormalized_posterior / P(E)

    Hanya penyakit dengan minimal satu gejala yang cocok yang masuk sebagai kandidat.
    Guard terhadap pembagian dengan nol diterapkan pada unnormalized == 0 dan P(E) == 0.
    Hasil diurutkan descending berdasarkan persentase sebelum dikembalikan.
    """

    # -- Build lookup: penyakit_id → {gejala_id: P(Eᵢ|H)} -------------------
    cond_map: dict[int, dict[int, float]] = {}
    for rule in aturan_list:
        pid = rule["penyakit_id"]
        gid = rule["gejala_id"]
        cp  = float(rule.get("conditional_probability", 0.0))
        cond_map.setdefault(pid, {})[gid] = cp

    # Prior seragam jika prior_probability belum diset
    total_penyakit = len(penyakit_list)
    uniform_prior  = 1.0 / total_penyakit if total_penyakit > 0 else 1.0

    # -- Pass 1: hitung unnormalized posterior per penyakit kandidat ----------
    candidates: list[dict] = []

    for p in penyakit_list:
        pid          = p["id"]
        gejala_rules = cond_map.get(pid, {})
        matched_ids  = [gid for gid in gejala_ids if gid in gejala_rules]

        # Lewati penyakit tanpa satu pun gejala yang cocok
        if not matched_ids:
            continue

        # P(H): prior probability
        prior = float(p.get("prior_probability") or 0.0)
        if prior <= 0.0:
            prior = uniform_prior

        # P(Eᵢ|H) untuk setiap gejala yang cocok
        nilai_gejala: List[float] = [gejala_rules[gid] for gid in matched_ids]

        # ∏ P(Eᵢ|H): hasil kali semua conditional probability
        likelihood_product = 1.0
        for cp in nilai_gejala:
            likelihood_product *= cp

        # P(H) × ∏ P(Eᵢ|H): unnormalized posterior
        unnormalized = prior * likelihood_product

        if unnormalized <= 0.0:
            logger.debug("Penyakit %s dilewati: unnormalized posterior = 0", pid)
            continue

        candidates.append({
            "penyakit":           p,
            "pid":                pid,
            "matched_ids":        matched_ids,
            "nilai_gejala":       nilai_gejala,
            "prior":              prior,
            "likelihood_product": likelihood_product,
            "unnormalized":       unnormalized,
        })

    if not candidates:
        return []

    # -- Pass 2: normalisasi P(E) = Σ unnormalized_posterior ------------------
    normalization_constant = sum(c["unnormalized"] for c in candidates)

    results: List[PenyakitHasil] = []

    for c in candidates:
        p = c["penyakit"]

        # P(H|E) = unnormalized / P(E)
        posterior = (
            c["unnormalized"] / normalization_constant
            if normalization_constant > 0.0
            else 0.0
        )

        persentase = round(posterior * 100, 4)
        status     = _get_status(posterior)

        results.append(
            PenyakitHasil(
                penyakit_id   = c["pid"],
                kode_penyakit = p.get("kode_penyakit", ""),
                nama_penyakit = p.get("nama_penyakit", ""),
                deskripsi     = p.get("deskripsi"),
                solusi        = p.get("solusi"),
                persentase    = persentase,
                status        = status,
                gejala_cocok  = c["matched_ids"],
                detail        = CalculationDetail(
                    nilai_gejala           = [round(v, 10) for v in c["nilai_gejala"]],
                    prior                  = round(c["prior"], 10),
                    likelihood_product     = round(c["likelihood_product"], 10),
                    unnormalized_posterior = round(c["unnormalized"], 10),
                    normalization_constant = round(normalization_constant, 10),
                    posterior              = round(posterior, 10),
                ),
            )
        )

    # Sort descending by persentase
    results.sort(key=lambda r: r.persentase, reverse=True)
    return results


# =============================================================================
# ENDPOINT
# =============================================================================

@router.post(
    "/",
    response_model=DiagnosaResponse,
    status_code=http_status.HTTP_200_OK,
    summary="Jalankan Diagnosa Teorema Bayes",
    description=(
        "Menerima daftar ID gejala yang dipilih pasien, lalu menghitung persentase "
        "kemungkinan setiap penyakit menggunakan metode Teorema Bayes sesuai modul "
        "universitas. Hasil diagnosa otomatis disimpan ke tabel riwayat_diagnosa."
    ),
)
def run_diagnosa(payload: DiagnosaRequest, current_user: UserModel = Depends(require_role(['user', 'admin']))) -> DiagnosaResponse:
    """
    Teorema Bayes diagnosis endpoint.

    1. Validate input - gejala_ids must not be empty.
    2. Deduplicate gejala_ids (preserve order, remove duplicates).
    3. Fetch all diseases from `penyakit`.
    4. Fetch all matching rules from `aturan` for the selected gejala.
    5. Run Teorema Bayes (semesta -> phi -> total_h -> bayes) per disease.
    6. Save history to `riwayat_diagnosa` (non-fatal on failure).
    7. Return sorted result list + riwayat_id.
    """

    # -- 1. Validation (Pydantic min_length=1 already guards empty lists) ------
    if not payload.gejala_ids:
        raise HTTPException(
            status_code=http_status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Daftar gejala tidak boleh kosong. Pilih minimal 1 gejala.",
        )

    # -- 2. Deduplicate while preserving order ---------------------------------
    seen_ids: set[int] = set()
    unique_gejala_ids: List[int] = []
    for gid in payload.gejala_ids:
        if gid not in seen_ids:
            seen_ids.add(gid)
            unique_gejala_ids.append(gid)

    try:
        # -- 3. Fetch all diseases ---------------------------------------------
        penyakit_list = _fetch_all_penyakit()
        if not penyakit_list:
            raise HTTPException(
                status_code=http_status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=(
                    "Basis data penyakit kosong. "
                    "Harap tambahkan data penyakit terlebih dahulu."
                ),
            )

        # -- 4. Fetch rules for selected symptoms ------------------------------
        aturan_list = _fetch_aturan_for_gejala(unique_gejala_ids)
        if not aturan_list:
            return DiagnosaResponse(
                success=True,
                message=(
                    "Tidak ada aturan yang cocok dengan gejala yang dipilih. "
                    "Pastikan data aturan (basis pengetahuan) sudah diisi."
                ),
                riwayat_id=None,
                total_gejala_dipilih=len(unique_gejala_ids),
                hasil=[],
            )

        # -- 5. Teorema Bayes calculation ----------------------------------------
        hasil = _run_teorema_bayes(penyakit_list, aturan_list, unique_gejala_ids)

        if not hasil:
            return DiagnosaResponse(
                success=True,
                message=(
                    "Tidak ada penyakit yang cocok dengan kombinasi gejala yang dipilih."
                ),
                riwayat_id=None,
                total_gejala_dipilih=len(unique_gejala_ids),
                hasil=[],
            )

        # -- 6. Save history (non-fatal) ---------------------------------------
        riwayat_id = _save_riwayat(current_user.id, unique_gejala_ids, hasil)

        # -- 7. Return result --------------------------------------------------
        top = hasil[0]
        return DiagnosaResponse(
            success=True,
            message=(
                f"Diagnosa berhasil dijalankan. "
                f"Kemungkinan tertinggi: {top.nama_penyakit} "
                f"({top.persentase:.2f}%) - {top.status}."
            ),
            riwayat_id=riwayat_id,
            total_gejala_dipilih=len(unique_gejala_ids),
            hasil=hasil,
        )

    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Unexpected error during diagnosa: %s", exc)
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Terjadi kesalahan internal pada mesin diagnosa: {exc}",
        )
