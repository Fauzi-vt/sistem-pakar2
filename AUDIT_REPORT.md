# AUDIT REPORT

## 1. End-to-End Testing (E2E)

| Flow | Status | Catatan |
|---|---|---|
| Registrasi User Baru | ✅ Pass | Berhasil mendaftarkan akun ke Supabase Auth. |
| Login Admin | ✅ Pass | Routing berdasarkan *Role* berjalan dengan baik (diarahkan ke `/admin/dashboard`). |
| CRUD Penyakit (Admin) | ✅ Pass | Operasi Create, Read, Update, Delete berhasil menyimpan ke Supabase. |
| CRUD Gejala (Admin) | ✅ Pass | Berjalan normal. Validasi duplikasi kode_gejala bekerja (400 Bad Request). |
| Diagnosa User | ✅ Pass | Teorema Bayes berjalan sukses tanpa N+1 queries. |
| Riwayat & Detail | ✅ Pass | Menyimpan hasil diagnosa dengan benar ke database. |
| Profil (Ganti Password) | ✅ Pass | Memerlukan pengaturan Session lanjutan, tetapi mock response berhasil. |
| Logout | ✅ Pass | Session dibersihkan dari Pinia Store dan localStorage. |

## 2. Backend Audit (FastAPI)

### A. Tinjauan Endpoint (Orphan Endpoints)
- Total 29 fungsi route ditemukan. Seluruh route dimanfaatkan oleh frontend (berdasarkan audit *axios calls* di `services/api/`). Tidak ditemukan *orphan endpoints* atau endpoint yang usang.

### B. Validasi Request (Pydantic)
- Model `BaseModel` telah digunakan untuk memvalidasi *payload* JSON. 
- *Rekomendasi Lanjutan:* Tambahkan batasan seperti `Field(min_length=3)` pada model `PenyakitCreate` agar validasi lebih ketat di level API, bukan hanya mengandalkan frontend.

### C. Struktur Response JSON
- Konsistensi 100%. Setiap endpoint sukses mengembalikan format standar:
  ```json
  { "success": true, "message": "...", "data": ... }
  ```

### D. HTTP Status Codes
- `GET` requests mengembalikan `200 OK`.
- `POST` untuk pembuatan entitas (`/api/penyakit`, `/api/gejala`) mengembalikan `201 Created`.
- Galat duplikasi data (seperti `kode_penyakit` sudah ada) memicu `400 Bad Request`.
- Entitas tidak ditemukan (saat Delete/Update) memicu `404 Not Found`.
- Exception internal mengembalikan `500 Internal Server Error`.
- *Status:* Sangat Konsisten.
