-- ==========================================
-- 03: CREATE INDEXES
-- ==========================================
-- Membuat index pada kolom-kolom yang sering digunakan pada query WHERE atau JOIN
-- untuk meningkatkan performa pembacaan data.

-- 1. Index untuk tabel Penyakit
CREATE INDEX IF NOT EXISTS idx_penyakit_kode ON public.penyakit(kode_penyakit);

-- 2. Index untuk tabel Gejala
CREATE INDEX IF NOT EXISTS idx_gejala_kode ON public.gejala(kode_gejala);

-- 3. Index untuk tabel Aturan
CREATE INDEX IF NOT EXISTS idx_aturan_penyakit_id ON public.aturan(penyakit_id);
CREATE INDEX IF NOT EXISTS idx_aturan_gejala_id ON public.aturan(gejala_id);

-- 4. Index untuk tabel Riwayat Diagnosa
CREATE INDEX IF NOT EXISTS idx_riwayat_user_id ON public.riwayat_diagnosa(user_id);
CREATE INDEX IF NOT EXISTS idx_riwayat_tanggal ON public.riwayat_diagnosa(created_at);
