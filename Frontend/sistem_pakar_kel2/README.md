# Sistem Pakar Diagnosa Penyakit THT (Frontend)

Repositori ini berisi kode frontend untuk **Sistem Pakar Diagnosis Penyakit Telinga, Hidung, dan Tenggorokan (THT) Menggunakan Metode Teorema Bayes Berbasis Web**, yang dibangun dengan **Vue 3 (Composition API)**, **Vite**, **Tailwind CSS v4**, dan **PrimeVue**.

---

## 🧠 Metode Sistem Pakar: Teorema Bayes

Sistem ini menggunakan **Teorema Bayes** sebagai metode inferensi untuk menghitung probabilitas suatu penyakit berdasarkan gejala yang dialami pasien.

### Formula

```
P(H|E) = P(E|H) × P(H) / P(E)
```

Keterangan:
- **P(H)** — *Prior Probability*: Probabilitas awal suatu penyakit terjadi sebelum mempertimbangkan gejala.
- **P(E|H)** — *Likelihood*: Probabilitas gejala muncul jika penyakit tersebut memang ada. Nilai ini diisi oleh pakar (dokter THT) sebagai **Certainty Factor** di basis aturan.
- **P(E)** — Probabilitas marginal dari gejala, digunakan sebagai faktor normalisasi.
- **P(H|E)** — *Posterior Probability*: Probabilitas suatu penyakit setelah mempertimbangkan gejala yang dipilih pasien. Inilah yang ditampilkan sebagai **Tingkat Keyakinan** pada hasil diagnosis.

### Alur Inferensi

1. Pasien memilih gejala yang dialami melalui antarmuka checklist.
2. Sistem mengambil semua aturan dari basis pengetahuan (relasi gejala–penyakit beserta bobot pakar).
3. Backend (FastAPI + Supabase) menghitung probabilitas posterior tiap penyakit menggunakan Teorema Bayes.
4. Hasil diurutkan dari probabilitas tertinggi ke terendah.
5. Diagnosis utama beserta kemungkinan penyakit lainnya ditampilkan kepada pengguna.

> **Catatan**: Proses perhitungan inferensi dilakukan sepenuhnya di sisi backend. Frontend hanya mengirimkan daftar ID gejala yang dipilih dan menampilkan hasil berupa nilai probabilitas posterior yang dikembalikan API.

---

## 🏗️ Arsitektur Frontend

Struktur folder terstandarisasi untuk pengembangan skala besar:

- **`src/assets/styles/`**: Pemisahan file CSS (`base.css`, `components.css`, `animations.css`, `utilities.css`).
- **`src/config/`**: Konfigurasi sentral aplikasi (`app.js`, dll.).
- **`src/plugins/`**: Inisialisasi library pihak ketiga (PrimeVue plugin, PrimeVue Aura theme, dll.).
- **`src/services/`**:
  - `http/axios.js`: Axios instance dengan integrasi `nprogress` global loading bar dan auth token interseptor.
  - `api/`: Berkas modular pemisah API call berdasarkan domain fitur.
- **`src/stores/`**: State management global menggunakan **Pinia** secara modular (`auth.store.js`, `penyakit.store.js`, `gejala.store.js`, dll.).
- **`src/middlewares/`**: Navigation guard modular untuk router (`auth.js` dan `guest.js`).
- **`src/schemas/`**: Skema validasi masukan form terpusat menggunakan **Yup** dan **VeeValidate**.

## 🎨 Fitur UI & UX
- **PrimeVue Components**: Menggunakan `<DataTable>`, `<Column>`, `<Toast>`, dan `<ConfirmDialog>` bawaan untuk menggantikan modal dan tabel kustom.
- **Lucide Icons**: Integrasi Lucide Icons untuk menggantikan Material Symbols demi konsistensi rendering visual.
- **Chart.js + vue-chartjs**: Visualisasi statistik diagnosa pada Dashboard Admin.

---

## 🚀 Cara Menjalankan

### Persiapan File Lingkungan
Salin file konfigurasi lingkungan:
```bash
cp .env.example .env
```
Sesuaikan `VITE_API_URL` dengan alamat backend Anda (default: `http://localhost:8000`).

### Pemasangan Modul
```bash
npm install
```

### Jalankan Server Pengembangan
```bash
npm run dev
```

### Build Produksi
```bash
npm run build
```

### Linter & Formatter
```bash
npm run lint
```
