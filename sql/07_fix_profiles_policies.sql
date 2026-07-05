-- ==========================================
-- 07: FIX PROFILES TABLE POLICIES
-- ==========================================
-- Masalah: Backend menggunakan anon key sehingga RLS memblokir:
-- 1. Admin tidak bisa melihat semua profil pengguna (GET /api/users)
-- 2. Registrasi tidak bisa menyimpan profil (INSERT diblokir)
-- 3. Backend tidak bisa update/delete profil pengguna lain
--
-- Solusi: Hapus policy lama yang terlalu ketat, tambah policy baru
-- yang mendukung operasi backend.
-- ==========================================

-- Hapus policy lama
DROP POLICY IF EXISTS "Profile Read Own Data" ON public.profiles;
DROP POLICY IF EXISTS "Profile Update Own Data" ON public.profiles;
DROP POLICY IF EXISTS "Profile Insert Own Data" ON public.profiles;
DROP POLICY IF EXISTS "Profile Delete Own Data" ON public.profiles;
DROP POLICY IF EXISTS "Profiles: Admin Read All" ON public.profiles;
DROP POLICY IF EXISTS "Profiles: Admin Write All" ON public.profiles;
DROP POLICY IF EXISTS "Profiles: User Read Own" ON public.profiles;
DROP POLICY IF EXISTS "Profiles: User Update Own" ON public.profiles;
DROP POLICY IF EXISTS "Profiles: Service Role Full Access" ON public.profiles;
DROP POLICY IF EXISTS "Profiles: Backend Insert" ON public.profiles;

-- ─── SOLUSI REKOMENDASI: Nonaktifkan RLS untuk tabel profiles ───
-- Backend server-side tidak perlu RLS karena sudah dilindungi oleh
-- middleware authentication FastAPI (JWT verification + role check).
ALTER TABLE public.profiles DISABLE ROW LEVEL SECURITY;
