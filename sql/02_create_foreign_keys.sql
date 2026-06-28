-- ==========================================
-- 02: CREATE FOREIGN KEYS & CASCADE DELETE
-- ==========================================
-- Skrip ini menghubungkan antar tabel dengan Foreign Key yang tepat,
-- serta mendefinisikan perilaku Cascade Delete agar tidak ada data yatim (orphan data).

-- 1. Tabel Aturan -> Penyakit
-- Jika suatu penyakit dihapus, maka aturan yang menggunakan penyakit tersebut otomatis dihapus
ALTER TABLE public.aturan
  DROP CONSTRAINT IF EXISTS fk_aturan_penyakit;

ALTER TABLE public.aturan
  ADD CONSTRAINT fk_aturan_penyakit
  FOREIGN KEY (penyakit_id)
  REFERENCES public.penyakit(id)
  ON DELETE CASCADE;

-- 2. Tabel Aturan -> Gejala
-- Jika suatu gejala dihapus, maka aturan yang menggunakan gejala tersebut otomatis dihapus
ALTER TABLE public.aturan
  DROP CONSTRAINT IF EXISTS fk_aturan_gejala;

ALTER TABLE public.aturan
  ADD CONSTRAINT fk_aturan_gejala
  FOREIGN KEY (gejala_id)
  REFERENCES public.gejala(id)
  ON DELETE CASCADE;

-- 3. Tabel Riwayat Diagnosa -> User (Auth)
-- Menggunakan UUID dari tabel auth.users bawaan Supabase
ALTER TABLE public.riwayat_diagnosa
  DROP CONSTRAINT IF EXISTS fk_riwayat_user;

ALTER TABLE public.riwayat_diagnosa
  ADD CONSTRAINT fk_riwayat_user
  FOREIGN KEY (user_id)
  REFERENCES auth.users(id)
  ON DELETE CASCADE;

-- 4. Tabel Profiles -> User (Auth)
-- Menghubungkan tabel profile custom ke auth.users
ALTER TABLE public.profiles
  DROP CONSTRAINT IF EXISTS fk_profiles_user;

ALTER TABLE public.profiles
  ADD CONSTRAINT fk_profiles_user
  FOREIGN KEY (id)
  REFERENCES auth.users(id)
  ON DELETE CASCADE;
