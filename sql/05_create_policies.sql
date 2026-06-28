-- ==========================================
-- 05: CREATE POLICIES (RLS)
-- ==========================================
-- Skrip ini mendefinisikan aturan akses per baris (Row Level Security).
-- Pastikan RLS sudah diaktifkan (04_enable_rls.sql) sebelum menjalankan ini.

-- Hapus policy lama (jika ada) untuk menghindari duplikasi
DROP POLICY IF EXISTS "Penyakit Read-Only for All" ON public.penyakit;
DROP POLICY IF EXISTS "Penyakit Write for Authenticated" ON public.penyakit;

DROP POLICY IF EXISTS "Gejala Read-Only for All" ON public.gejala;
DROP POLICY IF EXISTS "Gejala Write for Authenticated" ON public.gejala;

DROP POLICY IF EXISTS "Aturan Read-Only for All" ON public.aturan;
DROP POLICY IF EXISTS "Aturan Write for Authenticated" ON public.aturan;

DROP POLICY IF EXISTS "Riwayat Read Own Data" ON public.riwayat_diagnosa;
DROP POLICY IF EXISTS "Riwayat Insert Own Data" ON public.riwayat_diagnosa;
DROP POLICY IF EXISTS "Riwayat Delete Own Data" ON public.riwayat_diagnosa;

DROP POLICY IF EXISTS "Profile Read Own Data" ON public.profiles;
DROP POLICY IF EXISTS "Profile Update Own Data" ON public.profiles;

-- 1. Tabel Penyakit
-- Semua orang (anon & authenticated) bisa membaca data penyakit
CREATE POLICY "Penyakit Read-Only for All"
  ON public.penyakit FOR SELECT
  USING (true);

-- Hanya admin/authenticated yang bisa mengubah
CREATE POLICY "Penyakit Write for Authenticated"
  ON public.penyakit FOR ALL
  USING (auth.role() = 'authenticated');

-- 2. Tabel Gejala
CREATE POLICY "Gejala Read-Only for All"
  ON public.gejala FOR SELECT
  USING (true);

CREATE POLICY "Gejala Write for Authenticated"
  ON public.gejala FOR ALL
  USING (auth.role() = 'authenticated');

-- 3. Tabel Aturan
CREATE POLICY "Aturan Read-Only for All"
  ON public.aturan FOR SELECT
  USING (true);

CREATE POLICY "Aturan Write for Authenticated"
  ON public.aturan FOR ALL
  USING (auth.role() = 'authenticated');

-- 4. Tabel Riwayat Diagnosa
-- Hanya pengguna itu sendiri yang bisa melihat, menambah, atau menghapus riwayatnya
CREATE POLICY "Riwayat Read Own Data"
  ON public.riwayat_diagnosa FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Riwayat Insert Own Data"
  ON public.riwayat_diagnosa FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Riwayat Delete Own Data"
  ON public.riwayat_diagnosa FOR DELETE
  USING (auth.uid() = user_id);

-- 5. Tabel Profiles
CREATE POLICY "Profile Read Own Data"
  ON public.profiles FOR SELECT
  USING (auth.uid() = id);

CREATE POLICY "Profile Update Own Data"
  ON public.profiles FOR UPDATE
  USING (auth.uid() = id)
  WITH CHECK (auth.uid() = id);
