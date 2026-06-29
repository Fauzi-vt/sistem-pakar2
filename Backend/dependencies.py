import os
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from supabase import create_client, Client
from pydantic import BaseModel

# Inisialisasi HTTP Bearer
security = HTTPBearer()

# Re-inisialisasi Supabase khusus untuk fungsi utilitas auth
# Kita menggunakan SUPABASE_URL yang sama dengan main.py
from dotenv import load_dotenv
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL or "", SUPABASE_KEY or "")

class UserModel(BaseModel):
    id: str
    email: str
    role: str

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> UserModel:
    """
    Memvalidasi JWT yang dikirim via Authorization: Bearer <token>.
    Mendekode token melalui server Supabase untuk menjamin keaslian.
    """
    token = credentials.credentials
    try:
        # Panggil auth Supabase untuk memverifikasi token
        res = supabase.auth.get_user(token)
        if not res or not res.user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token sesi tidak valid atau sudah kadaluarsa (Expired JWT).",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        user_id = res.user.id
        email = res.user.email
        
        # Ambil role dari tabel profiles (bisa juga via res.user.app_metadata jika dikonfigurasi)
        profile_res = supabase.table("profiles").select("role").eq("id", user_id).execute()
        
        role = "user"
        if profile_res.data and len(profile_res.data) > 0:
            role = profile_res.data[0].get("role", "user")
            
        # Hardcode Admin Email untuk keamanan ekstra (Fallback)
        ADMIN_EMAILS = ["rifafauzi044@gmail.com"]
        if email in ADMIN_EMAILS:
            role = "admin"
            
        return UserModel(id=user_id, email=email or "", role=role)
        
    except Exception as e:
        # Jika error dari supabase auth, tangani dengan 401
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Autentikasi gagal: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )

def require_role(allowed_roles: list[str]):
    """
    Middleware Dependency Generator untuk Role-Based Access Control.
    Contoh penggunaan: Depends(require_role(["admin"]))
    """
    def role_checker(user: UserModel = Depends(get_current_user)):
        if user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Akses ditolak. Endpoint ini hanya untuk role: {', '.join(allowed_roles)}"
            )
        return user
    return role_checker
