-- ==========================================
-- 06: DATABASE HEALTH CHECK
-- ==========================================
-- Skrip ini digunakan untuk memverifikasi kondisi database secara keseluruhan,
-- seperti memeriksa jumlah baris, daftar tabel dengan RLS, dan index.

-- 1. Periksa Status RLS pada setiap tabel
SELECT 
    schemaname, 
    tablename, 
    rowsecurity 
FROM pg_tables 
WHERE schemaname = 'public'
ORDER BY tablename;

-- 2. Periksa Index yang tersedia di skema public
SELECT
    tablename,
    indexname,
    indexdef
FROM pg_indexes
WHERE schemaname = 'public'
ORDER BY tablename, indexname;

-- 3. Periksa Constraint (Foreign Key, Check)
SELECT 
    conrelid::regclass AS table_name,
    conname AS constraint_name,
    pg_get_constraintdef(c.oid) AS constraint_definition
FROM pg_constraint c
JOIN pg_namespace n ON n.oid = c.connamespace
WHERE n.nspname = 'public'
ORDER BY table_name;

-- 4. Statistik Jumlah Baris Data
SELECT 
    relname AS table_name, 
    n_live_tup AS row_count
FROM pg_stat_user_tables 
WHERE schemaname = 'public'
ORDER BY relname;
