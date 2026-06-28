import re

def patch():
    with open("main.py", "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Add Imports
    if "from dependencies import" not in content:
        content = content.replace(
            "from fastapi import FastAPI, HTTPException, status, Header",
            "from fastapi import FastAPI, HTTPException, status, Header, Depends\nfrom dependencies import get_current_user, require_role, UserModel"
        )
    
    # 2. Patch Admin endpoints
    admin_patterns = [
        (r"def create_penyakit\(data: PenyakitCreate\):", r"def create_penyakit(data: PenyakitCreate, current_admin: UserModel = Depends(require_role(['admin']))):"),
        (r"def update_penyakit\(penyakit_id: str, data: PenyakitUpdate\):", r"def update_penyakit(penyakit_id: str, data: PenyakitUpdate, current_admin: UserModel = Depends(require_role(['admin']))):"),
        (r"def delete_penyakit\(penyakit_id: str\):", r"def delete_penyakit(penyakit_id: str, current_admin: UserModel = Depends(require_role(['admin']))):"),
        
        (r"def create_gejala\(data: GejalaCreate\):", r"def create_gejala(data: GejalaCreate, current_admin: UserModel = Depends(require_role(['admin']))):"),
        (r"def update_gejala\(gejala_id: str, data: GejalaUpdate\):", r"def update_gejala(gejala_id: str, data: GejalaUpdate, current_admin: UserModel = Depends(require_role(['admin']))):"),
        (r"def delete_gejala\(gejala_id: str\):", r"def delete_gejala(gejala_id: str, current_admin: UserModel = Depends(require_role(['admin']))):"),
        
        (r"def bulk_save_aturan\(payload: AturanBulkSave\):", r"def bulk_save_aturan(payload: AturanBulkSave, current_admin: UserModel = Depends(require_role(['admin']))):"),
        (r"def create_aturan\(data: AturanRule\):", r"def create_aturan(data: AturanRule, current_admin: UserModel = Depends(require_role(['admin']))):"),
        (r"def update_aturan\(aturan_id: int, data: AturanRule\):", r"def update_aturan(aturan_id: int, data: AturanRule, current_admin: UserModel = Depends(require_role(['admin']))):"),
        (r"def delete_aturan\(aturan_id: int\):", r"def delete_aturan(aturan_id: int, current_admin: UserModel = Depends(require_role(['admin']))):"),
        
        (r"def get_dashboard_stats\(\):", r"def get_dashboard_stats(current_admin: UserModel = Depends(require_role(['admin']))):"),
        (r"def get_all_riwayat\(\):", r"def get_all_riwayat(current_admin: UserModel = Depends(require_role(['admin']))):"),
        (r"def delete_riwayat\(riwayat_id: str\):", r"def delete_riwayat(riwayat_id: str, current_admin: UserModel = Depends(require_role(['admin']))):"),
        
        (r"def get_all_users\(\):", r"def get_all_users(current_admin: UserModel = Depends(require_role(['admin']))):"),
        # update_user_role has specific args
        # delete_user has specific args
        (r"def seed_master_data\(\):", r"def seed_master_data(current_admin: UserModel = Depends(require_role(['admin']))):"),
    ]
    
    for old, new in admin_patterns:
        content = re.sub(old, new, content)

    # Manual regex for user endpoints
    content = re.sub(
        r"def update_user_role\(user_id: str, role: str\):",
        r"def update_user_role(user_id: str, role: str, current_admin: UserModel = Depends(require_role(['admin']))):",
        content
    )
    content = re.sub(
        r"def delete_user\(user_id: str\):",
        r"def delete_user(user_id: str, current_admin: UserModel = Depends(require_role(['admin']))):",
        content
    )
    
    # 3. Patch User Endpoints (Riwayat by User, Update Profile, Change Password)
    # get_riwayat_by_user
    content = re.sub(
        r"def get_riwayat_by_user\(user_id: str\):",
        r"def get_riwayat_by_user(user_id: str, current_user: UserModel = Depends(require_role(['user', 'admin']))):\n    if current_user.role != 'admin' and current_user.id != user_id:\n        raise HTTPException(status_code=403, detail='Akses ditolak')",
        content
    )
    
    # update_user_profile
    content = re.sub(
        r"def update_user_profile\(user_id: str, data: dict\):",
        r"def update_user_profile(user_id: str, data: dict, current_user: UserModel = Depends(require_role(['user', 'admin']))):\n    if current_user.role != 'admin' and current_user.id != user_id:\n        raise HTTPException(status_code=403, detail='Akses ditolak')",
        content
    )
    
    # change_password
    content = re.sub(
        r"def change_password\(data: PasswordChange\):",
        r"def change_password(data: PasswordChange, current_user: UserModel = Depends(require_role(['user', 'admin']))):\n    if current_user.role != 'admin' and current_user.id != data.user_id:\n        raise HTTPException(status_code=403, detail='Akses ditolak')",
        content
    )

    with open("main.py", "w", encoding="utf-8") as f:
        f.write(content)
        
    print("Patch applied to main.py")

if __name__ == "__main__":
    patch()
