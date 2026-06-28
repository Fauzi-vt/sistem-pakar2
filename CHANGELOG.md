# CHANGELOG

Dokumen ini mencatat seluruh perubahan, refactoring, dan audit yang telah dilakukan selama pengembangan akhir Sistem Pakar THT Menggunakan Metode Teorema Bayes.

## [1.0.0-rc.1] - 2026-06-28

### 🚀 Fitur Baru
- **Desain UI/UX Modern:** Merombak total antarmuka pengguna (`UserDashboard`, `UserDiagnosa`, `UserRiwayat`) menggunakan framework Vue 3 dengan komponen dari PrimeVue dan icon modern dari Lucide.
- **Skeleton Loading & Empty State:** Ditambahkan untuk meningkatkan pengalaman pengguna selama pengambilan data dari API, menghindari *layout shift*, dan menampilkan instruksi interaktif saat data kosong.
- **Dark Mode (Tema Gelap):** Menambahkan `ThemeSwitch.vue` di menu samping (`SidebarUser`) dan *header* admin yang mendukung sinkronisasi otomatis dengan pengaturan OS.

### 🛡️ Keamanan & Kinerja
- **Database RLS & Constraints:** Membuat dan membakukan 6 skrip SQL (di folder `sql/`) untuk integrasi `FOREIGN KEY`, `CASCADE DELETE`, `INDEX`, dan kebijakan keamanan `Row Level Security` (RLS) di Supabase.
- **Optimasi API Backend:** Menghapus endpoint usang dan memastikan seluruh *Response JSON* memiliki konsistensi tinggi (`success`, `message`, `data`) serta menggunakan HTTP Status Codes standar secara seragam.
- **Otorisasi Lanjutan:** Mengonfigurasi batasan akses agar Admin memiliki kontrol eksklusif terhadap entitas `Penyakit` dan `Gejala`, sementara User terisolasi pada akses data `Riwayat Diagnosa` pribadi mereka.

### 🐛 Perbaikan (Fixes)
- **Koreksi Terminologi:** Seluruh referensi "Naive Bayes", "Bayesian Classifier", atau "Certainty Factor" telah diganti secara sistematis di sisi frontend maupun backend menjadi "Teorema Bayes" dan "Probabilitas / Nilai Probabilitas" sesuai dengan nomenklatur medis/statistik skripsi.
- **Clean Code (0 Errors):** Audit via ESLint dan Vite Rollup Build berhasil menghilangkan peringatan mengenai modul yang tidak terpakai (orphan variables) dan merapikan pohon dependensi.
- Menambahkan dokumentasi ekstensif berupa `AUDIT_REPORT.md`, `SECURITY_REPORT.md`, dan `PERFORMANCE_REPORT.md`.
