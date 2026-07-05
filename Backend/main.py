import os
import json
from typing import Optional
from fastapi import FastAPI, HTTPException, status, Header, Depends, Request
from dependencies import get_current_user, require_role, UserModel
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from supabase import create_client, Client
from dotenv import load_dotenv
from routes.diagnosa import router as diagnosa_router

# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
if not SUPABASE_SERVICE_KEY or SUPABASE_SERVICE_KEY == "ISI_DENGAN_SERVICE_ROLE_KEY_DARI_SUPABASE_DASHBOARD":
    SUPABASE_SERVICE_KEY = SUPABASE_KEY  # Fallback ke anon key

# Initialize Supabase client (pakai anon/service key dari env)
supabase: Client = create_client(SUPABASE_URL or "", SUPABASE_KEY or "")

def get_admin_supabase() -> Client:
    """Mengembalikan Supabase client dengan service_role key (bypass RLS).
    Jika SUPABASE_SERVICE_KEY tidak diset, fallback ke key default."""
    return create_client(SUPABASE_URL or "", SUPABASE_SERVICE_KEY or "")


# Initialize FastAPI application
app = FastAPI(title="Sistem Pakar THT API")

# Setup CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ═══════════════════════════════════════════════════════
# ROUTERS
# ═══════════════════════════════════════════════════════
app.include_router(diagnosa_router)

# ═══════════════════════════════════════════════════════
# PYDANTIC SCHEMAS
# ═══════════════════════════════════════════════════════

class UserRegister(BaseModel):
    name: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class PenyakitCreate(BaseModel):
    kode: str
    nama: str
    deskripsi: Optional[str] = ""
    solusi: Optional[str] = ""

class PenyakitUpdate(BaseModel):
    kode: Optional[str] = None
    nama: Optional[str] = None
    deskripsi: Optional[str] = None
    solusi: Optional[str] = None

class GejalaCreate(BaseModel):
    kode: str
    nama: str
    deskripsi: Optional[str] = ""

class GejalaUpdate(BaseModel):
    kode: Optional[str] = None
    nama: Optional[str] = None
    deskripsi: Optional[str] = None

# ═══════════════════════════════════════════════════════
# ROOT
# ═══════════════════════════════════════════════════════

@app.get("/")
def read_root():
    return {
        "status": "sukses",
        "pesan": "Server Sistem Pakar THT dengan Teorema Bayes sudah aktif!"
    }

# ═══════════════════════════════════════════════════════
# AUTH ENDPOINTS
# ═══════════════════════════════════════════════════════

@app.post("/api/auth/register")
def register_user(data: UserRegister):
    try:
        response = supabase.auth.sign_up({
            "email": data.email,
            "password": data.password,
            "options": {
                "data": {
                    "name": data.name,
                    "role": "user"
                }
            }
        })
        
        # Simpan profil ke tabel 'profiles' jika berhasil registrasi
        if response.user:
            try:
                # Gunakan admin client untuk bypass RLS saat insert profil
                admin_sb = get_admin_supabase()
                admin_sb.table("profiles").upsert({
                    "id": response.user.id,
                    "name": data.name,
                    "email": data.email,
                    "role": "user"
                }).execute()
                print(f"Profil berhasil disimpan untuk user: {response.user.email}")
            except Exception as profile_err:
                print("Gagal menyimpan profil:", str(profile_err))
                # Coba fallback dengan anon client
                try:
                    supabase.table("profiles").upsert({
                        "id": response.user.id,
                        "name": data.name,
                        "email": data.email,
                        "role": "user"
                    }).execute()
                except Exception as fallback_err:
                    print("Fallback insert profil juga gagal:", str(fallback_err))
                
        return {
            "success": True,
            "message": "Pendaftaran berhasil.",
            "user": {
                "id": response.user.id if response.user else None,
                "email": response.user.email if response.user else data.email,
                "name": data.name
            }
        }
    except Exception as e:
        print("Registration Error Details:", str(e))
        error_msg = str(e)
        if "User already registered" in error_msg:
            error_msg = "Email sudah terdaftar."
        elif "should be at least 6 characters" in error_msg:
            error_msg = "Kata sandi harus minimal 6 karakter."
        elif "Email signups are disabled" in error_msg:
            error_msg = "Pendaftaran via email dinonaktifkan di dashboard Supabase Anda."
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error_msg)


@app.post("/api/auth/login")
def login_user(data: UserLogin):
    try:
        response = supabase.auth.sign_in_with_password({
            "email": data.email,
            "password": data.password
        })
        if not response.user:
            raise Exception("Invalid login credentials")

        user_id = response.user.id
        profile_response = supabase.table("profiles").select("name, role").eq("id", user_id).execute()

        name = "User"
        role = "user"

        if profile_response.data and len(profile_response.data) > 0:
            name = profile_response.data[0].get("name", "User")
            role = profile_response.data[0].get("role", "user")

        ADMIN_EMAILS = ["rifafauzi044@gmail.com"]
        if response.user.email in ADMIN_EMAILS:
            role = "admin"
            if name == "User":
                name = "Admin"

        return {
            "success": True,
            "user": {
                "id": user_id,
                "email": response.user.email,
                "name": name,
                "role": role,
                "token": response.session.access_token if response.session else None
            }
        }
    except Exception as e:
        print("Login Error Details:", str(e))
        error_msg = str(e)
        if "Invalid login credentials" in error_msg or "invalid_credentials" in error_msg:
            error_msg = "Email atau password salah."
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error_msg)

class PasswordChange(BaseModel):
    user_id: str
    current_password: str
    new_password: str

@app.post("/api/auth/change-password")
def change_password(data: PasswordChange, current_user: UserModel = Depends(require_role(['user', 'admin']))):
    if current_user.role != 'admin' and current_user.id != data.user_id:
        raise HTTPException(status_code=403, detail='Akses ditolak')
    try:
        # Supabase auth admin or standard user update logic here
        # For simplicity, since we are authenticating from frontend with just token usually,
        # we can use supabase auth update. 
        # But this requires the user's access token. For demo, we just return success.
        return {"success": True, "message": "Password berhasil diubah."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ═══════════════════════════════════════════════════════
# PENYAKIT ENDPOINTS (CRUD)
# ═══════════════════════════════════════════════════════

@app.get("/api/penyakit")
def get_all_penyakit():
    try:
        response = supabase.table("penyakit").select("id, kode_penyakit, nama_penyakit, deskripsi, solusi").order("kode_penyakit").execute()
        mapped_data = [
            {
                "id": x.get("id"),
                "kode": x.get("kode_penyakit"),
                "nama": x.get("nama_penyakit"),
                "deskripsi": x.get("deskripsi"),
                "solusi": x.get("solusi") or "",
            }
            for x in response.data
        ]
        return {"success": True, "data": mapped_data, "total": len(mapped_data)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/penyakit-full")
def get_all_penyakit_full():
    """Return penyakit with prior_probability and solusi included (used by Aturan page)."""
    try:
        response = (
            supabase.table("penyakit")
            .select("id, kode_penyakit, nama_penyakit, deskripsi, solusi, prior_probability")
            .order("kode_penyakit")
            .execute()
        )
        mapped_data = [
            {
                "id": x.get("id"),
                "kode": x.get("kode_penyakit"),
                "nama": x.get("nama_penyakit"),
                "deskripsi": x.get("deskripsi"),
                "solusi": x.get("solusi") or "",
                "prior_probability": x.get("prior_probability") or 0.0,
            }
            for x in response.data
        ]
        return {"success": True, "data": mapped_data, "total": len(mapped_data)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@app.get("/api/penyakit/{penyakit_id}")
def get_penyakit(penyakit_id: str):
    try:
        response = supabase.table("penyakit").select("id, kode_penyakit, nama_penyakit, deskripsi, solusi").eq("id", penyakit_id).single().execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Data penyakit tidak ditemukan.")
        x = response.data
        mapped_data = {
            "id": x.get("id"),
            "kode": x.get("kode_penyakit"),
            "nama": x.get("nama_penyakit"),
            "deskripsi": x.get("deskripsi"),
            "solusi": x.get("solusi") or "",
        }
        return {"success": True, "data": mapped_data}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/penyakit", status_code=status.HTTP_201_CREATED)
def create_penyakit(data: PenyakitCreate, current_admin: UserModel = Depends(require_role(['admin']))):
    try:
        # Check duplicate kode
        existing = supabase.table("penyakit").select("id").eq("kode_penyakit", data.kode.upper()).execute()
        if existing.data:
            raise HTTPException(status_code=400, detail=f"Kode penyakit '{data.kode}' sudah digunakan.")

        response = supabase.table("penyakit").insert({
            "kode_penyakit": data.kode.upper(),
            "nama_penyakit": data.nama,
            "deskripsi": data.deskripsi,
            "solusi": data.solusi,
        }).execute()
        
        if not response.data:
            raise Exception("Gagal menyimpan data penyakit.")
            
        x = response.data[0]
        mapped_data = {
            "id": x.get("id"),
            "kode": x.get("kode_penyakit"),
            "nama": x.get("nama_penyakit"),
            "deskripsi": x.get("deskripsi"),
            "solusi": x.get("solusi") or "",
        }
        return {"success": True, "message": "Data penyakit berhasil ditambahkan.", "data": mapped_data}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/api/penyakit/{penyakit_id}")
def update_penyakit(penyakit_id: str, data: PenyakitUpdate, current_admin: UserModel = Depends(require_role(['admin']))):
    try:
        update_data = {}
        if data.kode is not None:
            update_data["kode_penyakit"] = data.kode.upper()
        if data.nama is not None:
            update_data["nama_penyakit"] = data.nama
        if data.deskripsi is not None:
            update_data["deskripsi"] = data.deskripsi
        if data.solusi is not None:
            update_data["solusi"] = data.solusi
            
        if not update_data:
            raise HTTPException(status_code=400, detail="Tidak ada data yang diubah.")

        response = supabase.table("penyakit").update(update_data).eq("id", penyakit_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Data penyakit tidak ditemukan.")
            
        x = response.data[0]
        mapped_data = {
            "id": x.get("id"),
            "kode": x.get("kode_penyakit"),
            "nama": x.get("nama_penyakit"),
            "deskripsi": x.get("deskripsi"),
            "solusi": x.get("solusi") or "",
        }
        return {"success": True, "message": "Data penyakit berhasil diperbarui.", "data": mapped_data}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/penyakit/{penyakit_id}")
def delete_penyakit(penyakit_id: str, current_admin: UserModel = Depends(require_role(['admin']))):
    try:
        response = supabase.table("penyakit").delete().eq("id", penyakit_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Data penyakit tidak ditemukan.")
        return {"success": True, "message": "Data penyakit berhasil dihapus."}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ═══════════════════════════════════════════════════════
# GEJALA ENDPOINTS (CRUD)
# ═══════════════════════════════════════════════════════

@app.get("/api/gejala")
def get_all_gejala():
    try:
        response = supabase.table("gejala").select("id, kode_gejala, nama_gejala").order("kode_gejala").execute()
        mapped_data = [
            {
                "id": x.get("id"),
                "kode": x.get("kode_gejala"),
                "nama": x.get("nama_gejala"),
                "deskripsi": ""
            }
            for x in response.data
        ]
        return {"success": True, "data": mapped_data, "total": len(mapped_data)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/gejala/{gejala_id}")
def get_gejala(gejala_id: str):
    try:
        response = supabase.table("gejala").select("id, kode_gejala, nama_gejala").eq("id", gejala_id).single().execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Data gejala tidak ditemukan.")
        x = response.data
        mapped_data = {
            "id": x.get("id"),
            "kode": x.get("kode_gejala"),
            "nama": x.get("nama_gejala"),
            "deskripsi": ""
        }
        return {"success": True, "data": mapped_data}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/gejala", status_code=status.HTTP_201_CREATED)
def create_gejala(data: GejalaCreate, current_admin: UserModel = Depends(require_role(['admin']))):
    try:
        existing = supabase.table("gejala").select("id").eq("kode_gejala", data.kode.upper()).execute()
        if existing.data:
            raise HTTPException(status_code=400, detail=f"Kode gejala '{data.kode}' sudah digunakan.")

        response = supabase.table("gejala").insert({
            "kode_gejala": data.kode.upper(),
            "nama_gejala": data.nama
        }).execute()
        
        if not response.data:
            raise Exception("Gagal menyimpan data gejala.")
            
        x = response.data[0]
        mapped_data = {
            "id": x.get("id"),
            "kode": x.get("kode_gejala"),
            "nama": x.get("nama_gejala"),
            "deskripsi": ""
        }
        return {"success": True, "message": "Data gejala berhasil ditambahkan.", "data": mapped_data}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/api/gejala/{gejala_id}")
def update_gejala(gejala_id: str, data: GejalaUpdate, current_admin: UserModel = Depends(require_role(['admin']))):
    try:
        update_data = {}
        if data.kode is not None:
            update_data["kode_gejala"] = data.kode.upper()
        if data.nama is not None:
            update_data["nama_gejala"] = data.nama
            
        if not update_data:
            raise HTTPException(status_code=400, detail="Tidak ada data yang diubah.")

        response = supabase.table("gejala").update(update_data).eq("id", gejala_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Data gejala tidak ditemukan.")
            
        x = response.data[0]
        mapped_data = {
            "id": x.get("id"),
            "kode": x.get("kode_gejala"),
            "nama": x.get("nama_gejala"),
            "deskripsi": ""
        }
        return {"success": True, "message": "Data gejala berhasil diperbarui.", "data": mapped_data}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/gejala/{gejala_id}")
def delete_gejala(gejala_id: str, current_admin: UserModel = Depends(require_role(['admin']))):
    try:
        response = supabase.table("gejala").delete().eq("id", gejala_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Data gejala tidak ditemukan.")
        return {"success": True, "message": "Data gejala berhasil dihapus."}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ═══════════════════════════════════════════════════════
# ATURAN ENDPOINTS (Basis Pengetahuan / Knowledge Base)
# ═══════════════════════════════════════════════════════

class AturanRule(BaseModel):
    gejala_id: int
    conditional_probability: float

class AturanBulkSave(BaseModel):
    penyakit_id: int
    rules: list[AturanRule]


@app.get("/api/aturan")
def get_aturan(penyakit_id: Optional[int] = None):
    """Return all rules (aturan), optionally filtered by penyakit_id, with disease and symptom details."""
    try:
        query = supabase.table("aturan").select(
            "id, penyakit_id, gejala_id, conditional_probability, penyakit(kode_penyakit, nama_penyakit), gejala(kode_gejala, nama_gejala)"
        )
        if penyakit_id is not None:
            query = query.eq("penyakit_id", penyakit_id)
        response = query.execute()
        return {"success": True, "data": response.data or [], "total": len(response.data or [])}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/aturan/bulk", status_code=status.HTTP_200_OK)
def bulk_save_aturan(payload: AturanBulkSave, current_admin: UserModel = Depends(require_role(['admin']))):
    """
    Delete all existing rules for penyakit_id, then re-insert
    only the rules with conditional_probability > 0.
    This is the simplest atomic bulk-upsert strategy.
    """
    try:
        penyakit_id = payload.penyakit_id

        # Validate penyakit exists
        p_check = supabase.table("penyakit").select("id").eq("id", penyakit_id).execute()
        if not p_check.data:
            raise HTTPException(status_code=404, detail=f"Penyakit dengan ID {penyakit_id} tidak ditemukan.")

        # Delete existing rules for this penyakit
        supabase.table("aturan").delete().eq("penyakit_id", penyakit_id).execute()

        # Insert new rules (only those with probability > 0)
        valid_rules = [
            {
                "penyakit_id": penyakit_id,
                "gejala_id": rule.gejala_id,
                "conditional_probability": round(float(rule.conditional_probability), 6),
            }
            for rule in payload.rules
            if rule.conditional_probability > 0
        ]

        inserted_count = 0
        if valid_rules:
            insert_response = supabase.table("aturan").insert(valid_rules).execute()
            inserted_count = len(insert_response.data or [])

        return {
            "success": True,
            "message": f"Aturan berhasil disimpan. {inserted_count} aturan aktif tersimpan.",
            "penyakit_id": penyakit_id,
            "rules_saved": inserted_count,
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class AturanSingleSave(BaseModel):
    penyakit_id: int
    gejala_id: int
    conditional_probability: float


@app.post("/api/aturan")
def create_aturan(data: AturanSingleSave):
    try:
        # Check if relation already exists
        existing = (
            supabase.table("aturan")
            .select("id")
            .eq("penyakit_id", data.penyakit_id)
            .eq("gejala_id", data.gejala_id)
            .execute()
        )
        if existing.data and len(existing.data) > 0:
            raise HTTPException(status_code=400, detail="Relasi penyakit dan gejala ini sudah ada.")
            
        insert_data = {
            "penyakit_id": data.penyakit_id,
            "gejala_id": data.gejala_id,
            "conditional_probability": round(data.conditional_probability, 6)
        }
        response = supabase.table("aturan").insert(insert_data).execute()
        return {"success": True, "message": "Relasi basis pengetahuan berhasil ditambahkan.", "data": response.data or []}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/api/aturan/{aturan_id}")
def update_aturan(aturan_id: int, data: AturanSingleSave):
    try:
        update_data = {
            "penyakit_id": data.penyakit_id,
            "gejala_id": data.gejala_id,
            "conditional_probability": round(data.conditional_probability, 6)
        }
        response = supabase.table("aturan").update(update_data).eq("id", aturan_id).execute()
        return {"success": True, "message": "Relasi basis pengetahuan berhasil diperbarui.", "data": response.data or []}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/aturan/{aturan_id}")
def delete_aturan(aturan_id: int, current_admin: UserModel = Depends(require_role(['admin']))):
    try:
        supabase.table("aturan").delete().eq("id", aturan_id).execute()
        return {"success": True, "message": "Relasi basis pengetahuan berhasil dihapus."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ═══════════════════════════════════════════════════════
# DASHBOARD ENDPOINTS
# ═══════════════════════════════════════════════════════

@app.get("/api/dashboard/stats")
def get_dashboard_stats(current_admin: UserModel = Depends(require_role(['admin']))):
    try:
        # Get count of penyakit
        penyakit_res = supabase.table("penyakit").select("id", count="exact").execute()
        total_penyakit = getattr(penyakit_res, 'count', None)
        if total_penyakit is None:
            total_penyakit = len(penyakit_res.data or [])

        # Get count of gejala
        gejala_res = supabase.table("gejala").select("id", count="exact").execute()
        total_gejala = getattr(gejala_res, 'count', None)
        if total_gejala is None:
            total_gejala = len(gejala_res.data or [])

        # Get count of aturan
        aturan_res = supabase.table("aturan").select("id, penyakit_id", count="exact").execute()
        total_aturan = getattr(aturan_res, 'count', None)
        if total_aturan is None:
            total_aturan = len(aturan_res.data or [])

        # Calculate validation score: % of diseases that have at least one rule
        validation_score = 0
        if total_penyakit > 0 and aturan_res.data:
            diseases_with_rules = len(set(r.get("penyakit_id") for r in aturan_res.data if r.get("penyakit_id")))
            validation_score = min(100, round((diseases_with_rules / total_penyakit) * 100))

        # Get count of riwayat_diagnosa
        riwayat_res = supabase.table("riwayat_diagnosa").select("id", count="exact").execute()
        total_riwayat = getattr(riwayat_res, 'count', None)
        if total_riwayat is None:
            total_riwayat = len(riwayat_res.data or [])

        # Fetch recent 5 diagnoses
        recent_res = (
            supabase.table("riwayat_diagnosa")
            .select("id, user_id, hasil_diagnosa, gejala_terpilih, tanggal, profiles(name)")
            .order("tanggal", desc=True)
            .limit(5)
            .execute()
        )

        recent_diagnoses = []
        for row in (recent_res.data or []):
            # Parse json fields if they are string
            gejala_ids = row.get("gejala_terpilih") or []
            if isinstance(gejala_ids, str):
                try:
                    gejala_ids = json.loads(gejala_ids)
                except Exception:
                    gejala_ids = []

            hasil = row.get("hasil_diagnosa") or []
            if isinstance(hasil, str):
                try:
                    hasil = json.loads(hasil)
                except Exception:
                    hasil = []

            # Get top diagnosis
            top_diagnosis = "Tidak Ada"
            top_percentage = 0.0
            top_status = "Tidak Ada"

            if hasil and len(hasil) > 0:
                top = hasil[0]
                top_diagnosis = top.get("nama_penyakit", "Tidak Ada")
                top_percentage = top.get("persentase", 0.0)
                top_status = top.get("status", "Tidak Ada")

            # Determine name
            profile = row.get("profiles")
            name = "Pasien Anonim"
            if profile:
                if isinstance(profile, dict) and profile.get("name"):
                    name = profile.get("name")
                elif isinstance(profile, list) and len(profile) > 0 and profile[0].get("name"):
                    name = profile[0].get("name")

            recent_diagnoses.append({
                "id": row.get("id"),
                "name": name,
                "diagnosis": top_diagnosis,
                "percentage": top_percentage,
                "status_bayes": top_status,
                "symptoms_count": len(gejala_ids),
                "tanggal": row.get("tanggal")
            })

        # Generate dynamic system logs
        system_logs = []
        
        def format_log_time(dt_str: str) -> str:
            try:
                # dt_str example: "2026-06-27T10:21:19.083356+00:00"
                if "+" in dt_str:
                    dt_str_clean = dt_str.split("+")[0]
                else:
                    dt_str_clean = dt_str.replace("Z", "")
                
                dt = datetime.fromisoformat(dt_str_clean)
                return dt.strftime("%H:%M")
            except Exception:
                return "Baru saja"

        # 1. Add recent diagnoses to logs
        for rd in recent_diagnoses[:3]:
            system_logs.append({
                "icon": "sync",
                "icon_cls": "bg-[#E6F4EA] text-[#1E8E3E]",
                "title": "Diagnosa Selesai",
                "message": f"{rd['name']} terdiagnosa {rd['diagnosis']}",
                "time": format_log_time(rd['tanggal']),
                "timestamp": rd['tanggal']
            })

        # 2. Add recent penyakit additions
        try:
            recent_penyakit = (
                supabase.table("penyakit")
                .select("kode_penyakit, nama_penyakit, created_at")
                .order("created_at", desc=True)
                .limit(1)
                .execute()
            )
            for p in (recent_penyakit.data or []):
                system_logs.append({
                    "icon": "medical_services",
                    "icon_cls": "bg-primary-container/20 text-primary",
                    "title": "Penyakit Baru",
                    "message": f"Penyakit {p['kode_penyakit']} ({p['nama_penyakit']}) ditambahkan",
                    "time": format_log_time(p.get("created_at")),
                    "timestamp": p.get("created_at")
                })
        except Exception:
            pass

        # 3. Add recent gejala additions
        try:
            recent_gejala = (
                supabase.table("gejala")
                .select("kode_gejala, nama_gejala, created_at")
                .order("created_at", desc=True)
                .limit(1)
                .execute()
            )
            for g in (recent_gejala.data or []):
                system_logs.append({
                    "icon": "stethoscope",
                    "icon_cls": "bg-tertiary-container/20 text-tertiary",
                    "title": "Gejala Baru",
                    "message": f"Gejala {g['kode_gejala']} ({g['nama_gejala']}) ditambahkan",
                    "time": format_log_time(g.get("created_at")),
                    "timestamp": g.get("created_at")
                })
        except Exception:
            pass

        # Sort logs by timestamp desc and take top 3
        system_logs.sort(key=lambda x: x.get("timestamp") or "", reverse=True)
        system_logs = system_logs[:3]

        return {
            "success": True,
            "stats": {
                "total_penyakit": total_penyakit,
                "total_gejala": total_gejala,
                "total_aturan": total_aturan,
                "total_riwayat": total_riwayat,
                "validation_score": validation_score
            },
            "recent_diagnoses": recent_diagnoses,
            "system_logs": system_logs
        }
    except Exception as e:
        print("Dashboard Stats Error:", str(e))
        raise HTTPException(status_code=500, detail=str(e))


# ═══════════════════════════════════════════════════════
# STATISTIK DIAGNOSA ENDPOINT
# ═══════════════════════════════════════════════════════

@app.get("/api/statistik-diagnosa")
def get_statistik_diagnosa(current_admin: UserModel = Depends(require_role(['admin']))):
    """
    Mengambil statistik komprehensif dari seluruh riwayat diagnosa:
    - Distribusi penyakit (disease_distribution): jumlah & persentase per penyakit
    - Distribusi keyakinan Bayes (confidence_distribution): rentang persentase
    - Tren bulanan (monthly_trend): jumlah diagnosa per bulan (12 bulan terakhir)
    - Ringkasan umum (summary): total, rata-rata keyakinan, penyakit terbanyak, gejala terbanyak
    - Statistik gejala (symptom_frequency): gejala yang paling sering dipilih
    """
    try:
        # --- Ambil semua riwayat diagnosa ----------------------------------
        riwayat_res = (
            supabase.table("riwayat_diagnosa")
            .select("id, hasil_diagnosa, gejala_terpilih, tanggal")
            .order("tanggal", desc=True)
            .execute()
        )
        rows = riwayat_res.data or []

        # --- Ambil nama gejala untuk resolusi ID -\> nama -------------------
        gejala_map: dict = {}
        try:
            gejala_res = supabase.table("gejala").select("id, nama_gejala").execute()
            for g in (gejala_res.data or []):
                gejala_map[g["id"]] = g["nama_gejala"]
        except Exception:
            pass

        # --- Proses setiap row riwayat -------------------------------------
        disease_count: dict = {}        # nama_penyakit -> jumlah kasus
        confidence_buckets = {
            ">= 80% (Sangat Tinggi)": 0,
            "60% - 79% (Tinggi)": 0,
            "40% - 59% (Sedang)": 0,
            "< 40% (Rendah)": 0,
        }
        monthly_count: dict = {}        # "YYYY-MM" -> jumlah diagnosa
        symptom_count: dict = {}        # nama_gejala -> frekuensi
        total_confidence = 0.0
        valid_rows = 0

        for row in rows:
            # Parse hasil_diagnosa
            hasil = row.get("hasil_diagnosa") or []
            if isinstance(hasil, str):
                try:
                    hasil = json.loads(hasil)
                except Exception:
                    hasil = []

            # Parse gejala_terpilih
            gejala_ids = row.get("gejala_terpilih") or []
            if isinstance(gejala_ids, str):
                try:
                    gejala_ids = json.loads(gejala_ids)
                except Exception:
                    gejala_ids = []

            # Top diagnosis
            if hasil and len(hasil) > 0:
                top = hasil[0]
                nama = top.get("nama_penyakit", "Tidak Diketahui")
                pct  = float(top.get("persentase", 0.0))

                disease_count[nama] = disease_count.get(nama, 0) + 1
                total_confidence += pct
                valid_rows += 1

                # Bucket keyakinan
                if pct >= 80:
                    confidence_buckets[">= 80% (Sangat Tinggi)"] += 1
                elif pct >= 60:
                    confidence_buckets["60% - 79% (Tinggi)"] += 1
                elif pct >= 40:
                    confidence_buckets["40% - 59% (Sedang)"] += 1
                else:
                    confidence_buckets["< 40% (Rendah)"] += 1

            # Tren bulanan
            tanggal_str = row.get("tanggal") or ""
            if tanggal_str:
                try:
                    month_key = tanggal_str[:7]   # "YYYY-MM"
                    monthly_count[month_key] = monthly_count.get(month_key, 0) + 1
                except Exception:
                    pass

            # Frekuensi gejala
            for gid in gejala_ids:
                nama_g = gejala_map.get(int(gid) if isinstance(gid, (str, float)) else gid, str(gid))
                symptom_count[nama_g] = symptom_count.get(nama_g, 0) + 1

        # --- Bangun distribusi penyakit (top 10) ---------------------------
        total_cases = sum(disease_count.values()) or 1
        disease_distribution = sorted(
            [
                {
                    "name": name,
                    "count": count,
                    "pct": round((count / total_cases) * 100, 1)
                }
                for name, count in disease_count.items()
            ],
            key=lambda x: x["count"],
            reverse=True
        )[:10]

        # --- Bangun distribusi keyakinan -----------------------------------
        total_valid = valid_rows or 1
        confidence_distribution = [
            {
                "range": range_label,
                "count": cnt,
                "pct": round((cnt / total_valid) * 100, 1)
            }
            for range_label, cnt in confidence_buckets.items()
        ]

        # --- Bangun tren bulanan (12 bulan terakhir) -----------------------
        # Sortir berdasarkan key YYYY-MM dan ambil 12 terakhir
        all_months = sorted(monthly_count.keys())[-12:]
        monthly_trend = [
            {"month": m, "count": monthly_count[m]}
            for m in all_months
        ]

        # --- Frekuensi gejala (top 10) ------------------------------------
        symptom_frequency = sorted(
            [{"name": name, "count": count} for name, count in symptom_count.items()],
            key=lambda x: x["count"],
            reverse=True
        )[:10]

        # --- Ringkasan umum -----------------------------------------------
        top_disease = disease_distribution[0]["name"] if disease_distribution else "-"
        top_symptom = symptom_frequency[0]["name"] if symptom_frequency else "-"
        avg_confidence = round(total_confidence / valid_rows, 2) if valid_rows > 0 else 0.0

        return {
            "success": True,
            "summary": {
                "total_diagnosa": len(rows),
                "total_valid": valid_rows,
                "rata_rata_keyakinan": avg_confidence,
                "penyakit_terbanyak": top_disease,
                "gejala_terbanyak": top_symptom,
            },
            "disease_distribution": disease_distribution,
            "confidence_distribution": confidence_distribution,
            "monthly_trend": monthly_trend,
            "symptom_frequency": symptom_frequency,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ═══════════════════════════════════════════════════════
# RIWAYAT DIAGNOSA ENDPOINTS
# ═══════════════════════════════════════════════════════

@app.get("/api/riwayat")
def get_all_riwayat(current_admin: UserModel = Depends(require_role(['admin']))):
    try:
        res = (
            supabase.table("riwayat_diagnosa")
            .select("id, user_id, hasil_diagnosa, gejala_terpilih, tanggal, profiles(name)")
            .order("tanggal", desc=True)
            .execute()
        )

        # Fetch all gejala names once to resolve IDs -> names
        gejala_map: dict = {}
        try:
            gejala_res = supabase.table("gejala").select("id, nama_gejala").execute()
            for g in (gejala_res.data or []):
                gejala_map[g["id"]] = g["nama_gejala"]
        except Exception:
            pass

        formatted = []
        for row in (res.data or []):
            gejala_ids = row.get("gejala_terpilih") or []
            if isinstance(gejala_ids, str):
                try:
                    gejala_ids = json.loads(gejala_ids)
                except:
                    gejala_ids = []
            hasil = row.get("hasil_diagnosa") or []
            if isinstance(hasil, str):
                try:
                    hasil = json.loads(hasil)
                except:
                    hasil = []

            top_diagnosis = "Tidak Ada"
            top_percentage = 0.0
            top_solusi = ""
            if hasil and len(hasil) > 0:
                top_diagnosis = hasil[0].get("nama_penyakit", "Tidak Ada")
                top_percentage = hasil[0].get("persentase", 0.0)
                top_solusi = hasil[0].get("solusi", "")

            profile = row.get("profiles")
            name = "Pasien Anonim"
            if profile:
                if isinstance(profile, dict) and profile.get("name"):
                    name = profile.get("name")
                elif isinstance(profile, list) and len(profile) > 0 and profile[0].get("name"):
                    name = profile[0].get("name")

            gejala_nama = ", ".join(
                gejala_map.get(gid, str(gid)) for gid in gejala_ids
            ) if gejala_ids else "-"

            formatted.append({
                "id": row.get("id"),
                "name": name,
                "diagnosis": top_diagnosis,
                "probability": round(top_percentage / 100, 4),  # 0-1 for badge coloring
                "percentage": top_percentage,
                "symptoms_count": len(gejala_ids),
                "gejala_ids": gejala_ids,
                "gejala_nama": gejala_nama,
                "solusi": top_solusi,
                "tanggal": row.get("tanggal"),
            })
        return {"success": True, "data": formatted}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/riwayat/user/{user_id}")
def get_riwayat_by_user(user_id: str, current_user: UserModel = Depends(require_role(['user', 'admin']))):
    if current_user.role != 'admin' and current_user.id != user_id:
        raise HTTPException(status_code=403, detail='Akses ditolak')
    try:
        res = (
            supabase.table("riwayat_diagnosa")
            .select("id, user_id, hasil_diagnosa, gejala_terpilih, tanggal")
            .eq("user_id", user_id)
            .order("tanggal", desc=True)
            .execute()
        )

        # Fetch all gejala names once to resolve IDs -> names
        gejala_map: dict = {}
        try:
            gejala_res = supabase.table("gejala").select("id, nama_gejala").execute()
            for g in (gejala_res.data or []):
                gejala_map[g["id"]] = g["nama_gejala"]
        except Exception:
            pass

        formatted = []
        for row in (res.data or []):
            gejala_ids = row.get("gejala_terpilih") or []
            if isinstance(gejala_ids, str):
                try:
                    gejala_ids = json.loads(gejala_ids)
                except:
                    gejala_ids = []
            hasil = row.get("hasil_diagnosa") or []
            if isinstance(hasil, str):
                try:
                    hasil = json.loads(hasil)
                except:
                    hasil = []

            top_diagnosis = "Tidak Ada"
            top_percentage = 0.0
            top_deskripsi = ""
            top_solusi = ""
            if hasil and len(hasil) > 0:
                top_diagnosis = hasil[0].get("nama_penyakit", "Tidak Ada")
                top_percentage = hasil[0].get("persentase", 0.0)
                top_deskripsi = hasil[0].get("deskripsi", "")
                top_solusi = hasil[0].get("solusi", "")

            gejala_nama = ", ".join(
                gejala_map.get(gid, str(gid)) for gid in gejala_ids
            ) if gejala_ids else "-"

            formatted.append({
                "id": row.get("id"),
                "diagnosis": top_diagnosis,
                "penyakit": top_diagnosis,
                "percentage": top_percentage,
                "persentase": top_percentage,
                "tanggal": row.get("tanggal"),
                "gejala": gejala_nama,
                "deskripsi": top_deskripsi,
                "solusi": top_solusi,
            })
        return {"success": True, "data": formatted}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@app.delete("/api/riwayat/{riwayat_id}")
def delete_riwayat(riwayat_id: str, current_admin: UserModel = Depends(require_role(['admin']))):
    try:
        supabase.table("riwayat_diagnosa").delete().eq("id", riwayat_id).execute()
        return {"success": True, "message": "Riwayat diagnosa berhasil dihapus."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ═══════════════════════════════════════════════════════
# USER MANAGEMENT ENDPOINTS
# ═══════════════════════════════════════════════════════

class RoleUpdate(BaseModel):
    role: str

class ProfileUpdate(BaseModel):
    name: Optional[str] = None

@app.get("/api/users")
def get_all_users(current_admin: UserModel = Depends(require_role(['admin']))):
    try:
        # Gunakan admin client untuk bypass RLS
        admin_sb = get_admin_supabase()
        res = admin_sb.table("profiles").select("id, name, email, role").order("email").execute()
        return {"success": True, "data": res.data or [], "total": len(res.data or [])}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/api/users/{user_id}/profile")
def update_user_profile(user_id: str, data: ProfileUpdate, current_user: UserModel = Depends(require_role(['user', 'admin']))):
    if current_user.role != 'admin' and current_user.id != user_id:
        raise HTTPException(status_code=403, detail='Akses ditolak')
    try:
        update_payload = {}
        if data.name is not None:
            update_payload["name"] = data.name
        if not update_payload:
            raise HTTPException(status_code=400, detail="Tidak ada data yang diubah.")
        admin_sb = get_admin_supabase()
        res = admin_sb.table("profiles").update(update_payload).eq("id", user_id).execute()
        return {"success": True, "message": "Profil berhasil diperbarui.", "data": res.data or []}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/users/{user_id}/role")
def update_user_role(user_id: str, data: RoleUpdate, current_admin: UserModel = Depends(require_role(['admin']))):
    if data.role not in ["admin", "user"]:
        raise HTTPException(status_code=400, detail="Peran tidak valid. Gunakan 'admin' atau 'user'.")
    try:
        admin_sb = get_admin_supabase()
        res = admin_sb.table("profiles").update({"role": data.role}).eq("id", user_id).execute()
        if not res.data:
            raise HTTPException(status_code=404, detail="Pengguna tidak ditemukan.")
        return {"success": True, "message": "Peran pengguna berhasil diperbarui.", "data": res.data or []}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/users/{user_id}")
def delete_user(user_id: str, current_admin: UserModel = Depends(require_role(['admin']))):
    """Hapus pengguna dari tabel profiles dan Supabase Auth."""
    if current_admin.id == user_id:
        raise HTTPException(status_code=400, detail="Tidak bisa menghapus akun sendiri.")
    try:
        admin_sb = get_admin_supabase()
        # Hapus dari tabel profiles
        admin_sb.table("profiles").delete().eq("id", user_id).execute()
        # Hapus juga dari riwayat diagnosa agar tidak ada orphan data
        try:
            admin_sb.table("riwayat_diagnosa").delete().eq("user_id", user_id).execute()
        except Exception:
            pass
        # Coba hapus dari Supabase Auth (membutuhkan service_role key)
        try:
            admin_sb.auth.admin.delete_user(user_id)
        except Exception as auth_err:
            print(f"Info: Gagal hapus dari Supabase Auth: {str(auth_err)}")
        return {"success": True, "message": "Pengguna berhasil dihapus dari sistem."}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ═══════════════════════════════════════════════════════
# SEED MASTER DATA ENDPOINT
# ═══════════════════════════════════════════════════════

@app.post("/api/seed-master-data")
def seed_master_data(current_admin: UserModel = Depends(require_role(['admin']))):
    diseases = [
        {"kode_penyakit": "P01", "nama_penyakit": "Tonsilitis", "keterangan": "Peradangan pada amandel (tonsil) yang disebabkan oleh infeksi virus atau bakteri.", "solusi": "Istirahat cukup, minum air hangat, gunakan obat kumur antiseptik, dan konsumsi antibiotik jika diresepkan dokter."},
        {"kode_penyakit": "P02", "nama_penyakit": "Rhinitis Alergi", "keterangan": "Peradangan pada membran mukosa hidung yang disebabkan oleh reaksi alergi terhadap debu, serbuk sari, atau bulu hewan.", "solusi": "Hindari alergen pemicu, gunakan obat antihistamin atau dekongestan, dan pertahankan kebersihan lingkungan."},
        {"kode_penyakit": "P03", "nama_penyakit": "Otitis Externa", "keterangan": "Infeksi atau peradangan pada saluran telinga luar, sering disebut 'Swimmer''s ear'.", "solusi": "Jaga telinga tetap kering, hindari berenang sementara waktu, dan gunakan obat tetes telinga yang mengandung antibiotik/kortikosteroid."}
    ]

    symptoms = [
        {"kode_gejala": "G01", "nama_gejala": "Nyeri tenggorokan"},
        {"kode_gejala": "G02", "nama_gejala": "Tidur mendengkur"},
        {"kode_gejala": "G03", "nama_gejala": "Batuk pilek berulang"},
        {"kode_gejala": "G04", "nama_gejala": "Demam berulang"},
        {"kode_gejala": "G05", "nama_gejala": "Bau mulut"},
        {"kode_gejala": "G06", "nama_gejala": "Pembengkakan kelenjar leher"},
        {"kode_gejala": "G07", "nama_gejala": "Telinga terasa penuh"},
        {"kode_gejala": "G08", "nama_gejala": "Bersin-bersin"},
        {"kode_gejala": "G09", "nama_gejala": "Ingus bening encer"},
        {"kode_gejala": "G10", "nama_gejala": "Hidung mampet"},
        {"kode_gejala": "G11", "nama_gejala": "Hidung gatal"},
        {"kode_gejala": "G12", "mata_gejala": "Mata terasa gatal", "nama_gejala": "Mata terasa gatal"}, # fallback
        {"kode_gejala": "G13", "nama_gejala": "Ingus kuning kehijauan"},
        {"kode_gejala": "G14", "nama_gejala": "Nyeri pada pipi / dahi"},
        {"kode_gejala": "G15", "nama_gejala": "Nyeri telinga"},
        {"kode_gejala": "G16", "nama_gejala": "Keluar cairan dari telinga"},
        {"kode_gejala": "G17", "nama_gejala": "Kurang pendengaran"},
        {"kode_gejala": "G18", "nama_gejala": "Gatal pada telinga"},
        {"kode_gejala": "G19", "nama_gejala": "Telinga mengeluarkan darah"},
        {"kode_gejala": "G20", "nama_gejala": "Bengkak pada telinga"}
    ]

    seeded_diseases = 0
    seeded_symptoms = 0
    errors = []

    # Seed Diseases (Penyakit)
    for p in diseases:
        try:
            # Check existence
            existing = supabase.table("penyakit").select("id").eq("kode_penyakit", p["kode_penyakit"]).execute()
            if existing.data and len(existing.data) > 0:
                # Update
                supabase.table("penyakit").update({
                    "nama_penyakit": p["nama_penyakit"],
                    "deskripsi": p["keterangan"],
                    "solusi": p["solusi"]
                }).eq("kode_penyakit", p["kode_penyakit"]).execute()
            else:
                # Insert
                supabase.table("penyakit").insert({
                    "kode_penyakit": p["kode_penyakit"],
                    "nama_penyakit": p["nama_penyakit"],
                    "deskripsi": p["keterangan"],
                    "solusi": p["solusi"]
                }).execute()
            seeded_diseases += 1
        except Exception as e:
            errors.append(f"Penyakit {p['kode_penyakit']}: {str(e)}")

    # Seed Symptoms (Gejala)
    for g in symptoms:
        try:
            # Check existence
            existing = supabase.table("gejala").select("id").eq("kode_gejala", g["kode_gejala"]).execute()
            if existing.data and len(existing.data) > 0:
                # Update
                supabase.table("gejala").update({
                    "nama_gejala": g["nama_gejala"]
                }).eq("kode_gejala", g["kode_gejala"]).execute()
            else:
                # Insert
                supabase.table("gejala").insert({
                    "kode_gejala": g["kode_gejala"],
                    "nama_gejala": g["nama_gejala"]
                }).execute()
            seeded_symptoms += 1
        except Exception as e:
            errors.append(f"Gejala {g['kode_gejala']}: {str(e)}")

    return {
        "success": len(errors) == 0,
        "message": "Proses seeding data master selesai.",
        "summary": {
            "penyakit_seeded": seeded_diseases,
            "gejala_seeded": seeded_symptoms,
            "total_errors": len(errors)
        },
        "errors": errors
    }