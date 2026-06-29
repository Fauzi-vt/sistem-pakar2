-- ==========================================
-- 01: CHECK CONSTRAINTS
-- ==========================================
-- Skrip ini memastikan bahwa tipe data dan batasan logika (CHECK constraints)
-- diterapkan pada tabel-tabel utama untuk menjaga integritas data.

-- 1. Tabel Penyakit
-- Memastikan kode_penyakit berformat P diikuti angka (contoh: P01)
ALTER TABLE public.penyakit
  ADD CONSTRAINT chk_penyakit_kode CHECK (kode_penyakit ~ '^P[0-9]+$');

-- Memastikan prior_probability berada dalam rentang 0 hingga 1
ALTER TABLE public.penyakit
  ADD CONSTRAINT chk_prior_probability CHECK (prior_probability >= 0 AND prior_probability <= 1);

-- 2. Tabel Gejala
-- Memastikan kode_gejala berformat G diikuti angka (contoh: G01)
ALTER TABLE public.gejala
  ADD CONSTRAINT chk_gejala_kode CHECK (kode_gejala ~ '^G[0-9]+$');

-- 3. Tabel Aturan
-- Memastikan probabilitas (conditional probability) berada dalam rentang 0 hingga 1
ALTER TABLE public.aturan
  ADD CONSTRAINT chk_aturan_probabilitas CHECK (conditional_probability >= 0 AND conditional_probability <= 1);

-- Catatan: Jika query ini gagal karena ada data yang tidak memenuhi kriteria,
-- Anda harus membersihkan data (data cleansing) terlebih dahulu.
