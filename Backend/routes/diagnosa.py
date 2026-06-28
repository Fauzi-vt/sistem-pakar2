"""
diagnosa.py - Teorema Bayes Diagnosis Engine for Sistem Pakar THT
================================================================

Database Schema Reference:
  penyakit         : id (int), kode_penyakit, nama_penyakit, deskripsi, solusi,
                     prior_probability (float), created_at
  gejala           : id (int), kode_gejala, nama_gejala, created_at
  aturan           : id, penyakit_id (int), gejala_id (int),
                     conditional_probability (float), created_at
  riwayat_diagnosa : id, user_id (uuid|null), gejala_terpilih (json),
                     hasil_diagnosa (json), created_at

Algorithm (per disease):
  Let nilai_gejala = [conditional_probability for each matched symptom]

  Step 1 : semesta = sum(nilai_gejala)
  Step 2 : phi     = [nilai / semesta for nilai in nilai_gejala]
  Step 3 : total_h = sum(nilai_gejala[i] * phi[i] for i in range(n))
                     (Probabilitas Evidence)
  Step 4 : bayes   = sum( ((nilai_gejala[i] * phi[i]) / total_h) * nilai_gejala[i]
                          for i in range(n) )
           persentase = bayes * 100

Status mapping (based on raw bayes value 0.0-1.0):
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

from fastapi import APIRouter, HTTPException, status as http_status
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
    """Step-by-step breakdown of the Bayes calculation for one disease."""

    nilai_gejala: List[float]   # matched conditional_probability values
    semesta: float              # Step 1 : sum of nilai_gejala
    phi: List[float]            # Step 2 : normalised weights
    total_h: float              # Step 3 : probabilitas evidence
    bayes: float                # Step 4 : raw Bayes score (0.0 - 1.0)


class PenyakitHasil(BaseModel):
    """A single disease result entry returned after the Bayes calculation."""

    penyakit_id: int
    kode_penyakit: str
    nama_penyakit: str
    deskripsi: Optional[str] = None
    solusi: Optional[str] = None
    persentase: float           # bayes * 100, rounded to 4 dp
    status: str                 # string interpretation of the bayes score
    gejala_cocok: List[int]     # gejala_ids that matched this disease
    detail: CalculationDetail   # full step-by-step breakdown


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

def _get_status(bayes: float) -> str:
    """
    Map a raw Bayes score (0.0 - 1.0) to a human-readable status string.

      <= 0.2  ->  "Tidak Ada"
      <= 0.4  ->  "Mungkin"
      <= 0.6  ->  "Kemungkinan Besar"
      <  0.8  ->  "Hampir Pasti"
      >= 0.8  ->  "Pasti"
    """
    if bayes <= 0.2:
        return "Tidak Ada"
    if bayes <= 0.4:
        return "Mungkin"
    if bayes <= 0.6:
        return "Kemungkinan Besar"
    if bayes < 0.8:
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
    Each row: { penyakit_id, gejala_id, conditional_probability }
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
    Apply the university-specified Teorema Bayes algorithm for every disease.

    For each disease:
      1. Filter conditional_probability (Expert Values) from aturan where
         gejala_id matches the user's input -> stored as nilai_gejala.
      2. If len(nilai_gejala) > 0, apply the 4-step formula:

         semesta = sum(nilai_gejala)
         phi     = [nilai / semesta for nilai in nilai_gejala]
         total_h = sum(nilai_gejala[i] * phi[i] for i in range(n))
         bayes   = sum(((nilai_gejala[i] * phi[i]) / total_h) * nilai_gejala[i]
                       for i in range(n))
         persentase = bayes * 100

    Division-by-zero guards are applied at both semesta == 0 and total_h == 0.
    Results are sorted descending by persentase before returning.
    """

    # Build lookup: penyakit_id -> {gejala_id: conditional_probability}
    cond_map: dict[int, dict[int, float]] = {}
    for rule in aturan_list:
        pid = rule["penyakit_id"]
        gid = rule["gejala_id"]
        cp  = float(rule.get("conditional_probability", 0.0))
        cond_map.setdefault(pid, {})[gid] = cp

    selected_set = set(gejala_ids)
    results: List[PenyakitHasil] = []

    for p in penyakit_list:
        pid = p["id"]

        # Filter matching conditional probabilities for this disease
        gejala_rules = cond_map.get(pid, {})
        matched_ids  = [gid for gid in gejala_ids if gid in gejala_rules]

        # Only process diseases that have at least one matching symptom rule
        if not matched_ids:
            continue

        # nilai_gejala: list of expert conditional_probability for matched symptoms
        nilai_gejala: List[float] = [gejala_rules[gid] for gid in matched_ids]
        n = len(nilai_gejala)

        # -- Step 1: semesta (universe / total of expert values) ---------------
        semesta = sum(nilai_gejala)
        if semesta == 0.0:
            logger.debug("Disease %s skipped: semesta == 0", pid)
            continue

        # -- Step 2: phi (normalised weight per symptom) -----------------------
        phi = [nilai / semesta for nilai in nilai_gejala]

        # -- Step 3: total_h (Probabilitas Evidence) ---------------------------
        total_h = sum(nilai_gejala[i] * phi[i] for i in range(n))
        if total_h == 0.0:
            logger.debug("Disease %s skipped: total_h == 0", pid)
            continue

        # -- Step 4: bayes score -----------------------------------------------
        bayes = sum(
            ((nilai_gejala[i] * phi[i]) / total_h) * nilai_gejala[i]
            for i in range(n)
        )

        persentase = round(bayes * 100, 4)
        status     = _get_status(bayes)

        results.append(
            PenyakitHasil(
                penyakit_id   = pid,
                kode_penyakit = p.get("kode_penyakit", ""),
                nama_penyakit = p.get("nama_penyakit", ""),
                deskripsi     = p.get("deskripsi"),
                solusi        = p.get("solusi"),
                persentase    = persentase,
                status        = status,
                gejala_cocok  = matched_ids,
                detail        = CalculationDetail(
                    nilai_gejala = [round(v, 10) for v in nilai_gejala],
                    semesta      = round(semesta, 10),
                    phi          = [round(v, 10) for v in phi],
                    total_h      = round(total_h, 10),
                    bayes        = round(bayes, 10),
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
def run_diagnosa(payload: DiagnosaRequest) -> DiagnosaResponse:
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
        riwayat_id = _save_riwayat(payload.user_id, unique_gejala_ids, hasil)

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
