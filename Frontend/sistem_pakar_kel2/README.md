# Sistem Pakar Diagnosa Penyakit THT (Frontend)

Repositori ini berisi kode frontend untuk sistem pakar diagnosa penyakit THT menggunakan metode **Bayes & Certainty Factor**, yang dibangun dengan **Vue 3 (Composition API)**, **Vite**, **Tailwind CSS v4**, dan **PrimeVue**.

## 🏗️ Refactored Architecture

Struktur folder sekarang terstandarisasi untuk kenyamanan pengembangan skala besar:
- **`src/assets/styles/`**: Pemisahan styles CSS (`base.css`, `components.css`, `animations.css`, `utilities.css`).
- **`src/config/`**: Konfigurasi sentral aplikasi (`app.js`, dll.).
- **`src/plugins/`**: Inisialisasi library pihak ketiga (PrimeVue plugin, PrimeVue Aura theme, dll.).
- **`src/services/`**:
  - `http/axios.js`: Axios instance dengan integrasi `nprogress` global loading bar dan auth tokens interseptor.
  - `api/`: Berkas modular pemisah API call berdasarkan domain fitur.
- **`src/stores/`**: State management global menggunakan **Pinia** secara modular (`auth.store.js`, `penyakit.store.js`, `gejala.store.js`, dll.).
- **`src/middlewares/`**: Navigation guard modular untuk router (`auth.js` dan `guest.js`).
- **`src/schemas/`**: Skema validasi masukan form terpusat menggunakan **Yup** dan **VeeValidate**.

## 🎨 UI & UX Features
- **PrimeVue Components**: Menggunakan `<DataTable>`, `<Column>`, `<Toast>`, dan `<ConfirmDialog>` bawaan untuk menggantikan modal dan tabel kustom.
- **Lucide Icons**: Integrasi Lucide Icons untuk menggantikan Material Symbols demi konsistensi rendering visual.
- **Visual Chart**: Statistik diagnosa THT di Dashboard Admin dirender dengan visual **Chart.js** & **vue-chartjs**.

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
