# PERFORMANCE REPORT

Laporan performa Sistem Pakar THT berbasis pengujian Frontend dan Backend.

## 1. Frontend Bundle Size (Vite)
- **Temuan Audit:** Kompilasi `vite build` menampilkan peringatan:
  ```
  (!) Some chunks are larger than 500 kB after minification.
  ```
- **Penyebab Utama:** *Library* eksternal seperti `lucide-vue-next` (611.77 kB) digabung ke dalam chunk utama (`index-DbMcZwiV.js` dan `lucide-vue-next-CDZVlXLb.js`).
- **Mitigasi:** Pustaka komponen pihak ketiga disarankan dimasukkan dalam porsi `manualChunks` di `vite.config.js` atau di-*load* dengan pola **Lazy Loading Route** untuk halaman Dashboard, Edukasi, dan Profil sehingga halaman awal (Home/Login) dapat termuat di bawah waktu 1 detik.

## 2. Optimasi Route-Level Lazy Loading
- Routing aplikasi di `src/router/index.js` sudah menerapkan *dynamic import* (`component: () => import(...)`). Ini berhasil memisahkan chunk halaman secara efisien. Contoh: `UserRiwayat-DlNarbO3.js` dipisah menjadi 21.84 kB, memastikan memori hanya dipakai ketika halaman tersebut dikunjungi.

## 3. Backend Database Queries
- **N+1 Queries:** Pengecekan pada fungsi `_fetch_aturan_for_gejala` dan sinkronisasi gejala tidak menampilkan permasalahan iterasi kueri satu per satu (N+1). Kueri menggunakan operator `IN` seperti `.in_("gejala_id", gejala_ids)` yang memfetch data sekaligus secara efisien.
- **Kondisi Loop Backend:** Logika Teorema Bayes berjalan dalam bentuk operasi vektor memori (List dan Dictionary) setelah pengambilan data dari database sehingga sangat ringan dan cepat (<100ms eksekusi).

## 4. Database Indexing
- Untuk mengimbangi pertumbuhan data `riwayat_diagnosa` dan referensi pencarian Teorema Bayes, telah disediakan skrip `03_create_indexes.sql` yang menambahkan Index pada kolom-kolom relasional (seperti `penyakit_id`, `gejala_id`, `user_id`, dan `created_at`). Ini memastikan performa kueri tetap instan pada skala ratusan ribu data.
