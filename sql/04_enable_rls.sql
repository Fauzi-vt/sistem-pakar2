-- ==========================================
-- 04: ENABLE ROW LEVEL SECURITY (RLS)
-- ==========================================
-- Skrip ini memastikan RLS aktif pada seluruh tabel di skema public
-- agar akses data terlindungi secara default sebelum Policy ditambahkan.

ALTER TABLE public.penyakit ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.gejala ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.aturan ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.riwayat_diagnosa ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;
