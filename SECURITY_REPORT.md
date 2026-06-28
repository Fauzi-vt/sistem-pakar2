# SECURITY REPORT

Laporan ini menguraikan analisis keamanan dari Sistem Pakar THT dan langkah-langkah mitigasi yang diperlukan sebelum perilisan.

## 1. Supabase Row Level Security (RLS)
- **Status:** Diaktifkan melalui skrip `04_enable_rls.sql` dan `05_create_policies.sql`.
- **Implementasi:** 
  - Tabel Referensi (`penyakit`, `gejala`, `aturan`) dapat dibaca secara publik, namun hanya dapat dimodifikasi oleh Admin.
  - Tabel Sensitif (`riwayat_diagnosa`, `profiles`) menerapkan *Policy* ketat di mana pengguna hanya dapat melakukan `SELECT`, `INSERT`, `UPDATE`, dan `DELETE` pada data miliknya sendiri (menggunakan `auth.uid() = user_id`).

## 2. Pengelolaan Kunci (Key Management)
- **Frontend:** Lingkungan Vue aman karena tidak pernah mengekspos *Service Role Key* atau bahkan *Anon Key*. Frontend mendelegasikan transaksi data sepenuhnya melalui backend FastAPI.
- **Backend:** 
  - Backend saat ini menggunakan kunci Supabase yang dapat membaca profil JWT (`Anon Key`). Karena backend memproses rute krusial, sangat disarankan untuk menggunakan **Service Role Key** di sisi server (FastAPI) agar tidak terhalang oleh RLS ketika melakukan operasi sistem tingkat tinggi, ATAU meneruskan JWT pengguna dari Frontend ke Supabase.
  - **Tindakan:** Menggunakan *Service Role Key* pada variabel environment `SUPABASE_KEY` di backend.

## 3. Otentikasi dan Otorisasi API (FastAPI)
- **Temuan:** Routing untuk operasi CRUD pada Penyakit, Gejala, dan Aturan saat ini belum menggunakan `Depends(verify_token)` dari JWT.
- **Risiko:** Endpoint dapat dipanggil dari luar aplikasi jika URL API diketahui.
- **Rekomendasi:** Terapkan Dependensi JWT bawaan atau Middleware untuk mevalidasi token Authorization Bearer agar endpoint `/api/penyakit` (POST, PUT, DELETE) hanya dapat diakses oleh Admin.

## 4. Perlindungan Frontend & HTTP
- **CORS:** Middleware FastAPI mengizinkan semua origin (`allow_origins=["*"]`). Saat perilisan di *production*, ganti array ini dengan domain spesifik frontend.
- **Vulnerabilitas XSS/CSRF:** Penggunaan framework Vue modern meminimalisir risiko XSS karena *template binding* secara otomatis melakukan validasi karakter (escaping). Tidak ada risiko serius yang terdeteksi.
