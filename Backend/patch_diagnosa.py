import re

def patch():
    with open("routes/diagnosa.py", "r", encoding="utf-8") as f:
        content = f.read()

    # Add dependencies
    if "from dependencies import" not in content:
        content = content.replace(
            "from fastapi import APIRouter, HTTPException, status as http_status",
            "from fastapi import APIRouter, HTTPException, Depends, status as http_status\nfrom dependencies import get_current_user, require_role, UserModel"
        )

    # Modify DiagnosaRequest (Remove user_id field)
    # Using regex to remove user_id field
    content = re.sub(
        r"    user_id: Optional\[str\] = Field\([^)]+\)\n",
        "",
        content,
        flags=re.MULTILINE
    )

    # Modify run_diagnosa signature
    content = re.sub(
        r"def run_diagnosa\(payload: DiagnosaRequest\) -> DiagnosaResponse:",
        r"def run_diagnosa(payload: DiagnosaRequest, current_user: UserModel = Depends(require_role(['user', 'admin']))) -> DiagnosaResponse:",
        content
    )

    # Modify _save_riwayat call
    content = re.sub(
        r"riwayat_id = _save_riwayat\(payload\.user_id, unique_gejala_ids, hasil\)",
        r"riwayat_id = _save_riwayat(current_user.id, unique_gejala_ids, hasil)",
        content
    )

    with open("routes/diagnosa.py", "w", encoding="utf-8") as f:
        f.write(content)
        
    print("Patch applied to diagnosa.py")

if __name__ == "__main__":
    patch()
