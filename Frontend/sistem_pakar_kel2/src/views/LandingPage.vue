<template>
  <div class="bg-surface text-on-surface selection:bg-primary-fixed selection:text-on-primary-fixed min-h-screen flex flex-col font-sans">

    <!-- Top Navigation Bar -->
    <header class="fixed top-0 left-0 w-full z-50 flex justify-between items-center px-6 md:px-8 h-16 bg-surface/80 backdrop-blur-md border-b border-outline-variant/30 shadow-sm transition-all duration-300">
      <div class="flex items-center gap-2">
        <span class="material-symbols-outlined text-primary text-3xl" style="font-variation-settings: 'FILL' 1;">stethoscope</span>
        <span class="font-headline-sm text-headline-sm font-bold text-primary">ENT Expert</span>
      </div>
      <nav class="hidden md:flex gap-6 items-center">
        <a class="font-body-sm text-body-sm text-primary border-b-2 border-primary pb-1" href="#">Beranda</a>
        <a class="font-body-sm text-body-sm text-on-surface-variant hover:text-primary transition-colors" href="#tentang-kami">Tentang Kami</a>
        <a class="font-body-sm text-body-sm text-on-surface-variant hover:text-primary transition-colors" href="#metodologi">Metodologi</a>
      </nav>
      <div class="flex items-center gap-4">
        <router-link to="/login" class="hidden sm:block font-label-md text-label-md text-primary hover:bg-surface-container-high/50 px-4 py-2 rounded-lg transition-all">Masuk</router-link>
        <router-link to="/register" class="bg-primary text-on-primary px-5 py-2 rounded-lg font-label-md text-label-md hover:shadow-lg hover:shadow-primary/20 transition-all">Daftar</router-link>
      </div>
    </header>

    <main class="pt-16 flex-1">
      <!-- Hero Section -->
      <section class="relative min-h-[90vh] flex items-center overflow-hidden">
        <!-- Background Image with Overlay -->
        <div class="absolute inset-0 z-0">
          <img alt="Medical Hero" class="w-full h-full object-cover" src="https://lh3.googleusercontent.com/aida-public/AB6AXuB-xCc1yTLJ4425bI0axQhZVjwBVEzRm8KWIxZH5Og_Jm1dSoESSJBVEvv_LveL0oNBFDhnQppgHvvMk7j2xAl_VUyZR1c47h1H1QLdGr9Zyq71-rhlagqXHv6YDYhv7RZadUaT3qJnhFCh-MmwTaE0NO6m4pNW7SzyawDJNTM_b-0JVVU0iWwWRh55knfOFaUnxVPcffrWxiWZHtEC2JYujtPQoVbQeAyWlbMAP777si2-Z5d_UoXuRYxlwZH2LDM82RNffxVmm5Y8"/>
          <div class="absolute inset-0 bg-gradient-to-r from-surface via-surface/90 to-transparent"></div>
        </div>

        <div class="container mx-auto px-6 md:px-8 relative z-10 grid md:grid-cols-2 gap-8">
          <div class="max-w-xl flex flex-col justify-center gap-6">
            <div class="inline-flex items-center gap-1.5 bg-primary-container/30 text-primary px-3 py-1 rounded-full w-fit">
              <span class="material-symbols-outlined text-sm" style="font-variation-settings: 'FILL' 1;">bolt</span>
              <span class="text-label-sm font-label-sm uppercase tracking-wider text-xs font-semibold">Sistem pakar THT</span>
            </div>

            <h1 class="font-display text-4xl md:text-5xl font-bold text-on-surface leading-tight">
              Solusi Pakar untuk <span class="text-primary">Kesehatan THT</span> Anda
            </h1>

            <p class="font-body-lg text-body-lg text-on-surface-variant leading-relaxed">
              Diagnosis cerdas menggunakan Teorema Bayes untuk mendukung keputusan klinis yang cepat dan akurat. Dirancang khusus untuk efisiensi praktik dokter spesialis THT.
            </p>

            <div class="flex flex-wrap gap-4 mt-2">
              <router-link to="/diagnosa" class="bg-primary text-on-primary px-6 py-3 rounded-xl font-headline-sm text-sm font-bold flex items-center gap-2 hover:scale-[1.02] transition-transform shadow-xl shadow-primary/20">
                Mulai Konsultasi
                <span class="material-symbols-outlined">arrow_forward</span>
              </router-link>
              <a href="#alur-kerja" class="bg-white border border-outline-variant text-on-surface-variant px-6 py-3 rounded-xl font-headline-sm text-sm font-bold hover:bg-surface-container-low transition-colors text-center">
                Pelajari Lebih Lanjut
              </a>
            </div>

            <div class="flex items-center gap-8 mt-6 pt-6 border-t border-outline-variant/30">
              <div class="flex flex-col">
                <span class="font-headline-md text-xl font-bold text-primary">98%</span>
                <span class="font-label-sm text-xs text-on-surface-variant">Akurasi Diagnosis</span>
              </div>
              <div class="flex flex-col">
                <span class="font-headline-md text-xl font-bold text-primary">10k+</span>
                <span class="font-label-sm text-xs text-on-surface-variant">Pasien Terlayani</span>
              </div>
              <div class="flex flex-col">
                <span class="font-headline-md text-xl font-bold text-primary">500+</span>
                <span class="font-label-sm text-xs text-on-surface-variant">Dokter Aktif</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- How It Works (Bento Grid Style) -->
      <section id="alur-kerja" class="py-16 bg-white">
        <div class="container mx-auto px-6 md:px-8">
          <div class="text-center max-w-2xl mx-auto mb-12">
            <h2 class="font-headline-lg text-3xl font-bold text-on-surface mb-4">Alur Kerja Sistem Kami</h2>
            <p class="font-body-md text-body-md text-on-surface-variant">Proses diagnosis yang sederhana namun didukung oleh mesin inferensi medis yang kompleks.</p>
          </div>

          <div class="grid md:grid-cols-3 gap-6">
            <!-- Step 1 -->
            <div class="glass-card p-6 rounded-2xl group hover:-translate-y-2 transition-all duration-300">
              <div class="w-14 h-14 bg-surface-container-highest rounded-xl flex items-center justify-center mb-6 group-hover:bg-primary-container transition-colors">
                <span class="material-symbols-outlined text-primary text-3xl">list_alt</span>
              </div>
              <div class="mb-2 text-primary font-bold text-sm">Langkah 1</div>
              <h3 class="font-headline-sm text-lg font-bold mb-2">Input Gejala</h3>
              <p class="font-body-sm text-body-sm text-on-surface-variant">Pilih gejala klinis yang dialami melalui antarmuka intuitif kami yang mencakup telinga, hidung, dan tenggorokan.</p>
            </div>

            <!-- Step 2 -->
            <div class="glass-card p-6 rounded-2xl group hover:-translate-y-2 transition-all duration-300">
              <div class="w-14 h-14 bg-surface-container-highest rounded-xl flex items-center justify-center mb-6 group-hover:bg-primary-container transition-colors">
                <span class="material-symbols-outlined text-primary text-3xl">psychology</span>
              </div>
              <div class="mb-2 text-primary font-bold text-sm">Langkah 2</div>
              <h3 class="font-headline-sm text-lg font-bold mb-2">Analisis Sistem</h3>
              <p class="font-body-sm text-body-sm text-on-surface-variant">Mesin inferensi Teorema Bayes memproses input Anda terhadap basis pengetahuan medis yang luas secara real-time, menghitung probabilitas posterior setiap penyakit.</p>
            </div>

            <!-- Step 3 -->
            <div class="glass-card p-6 rounded-2xl group hover:-translate-y-2 transition-all duration-300">
              <div class="w-14 h-14 bg-surface-container-highest rounded-xl flex items-center justify-center mb-6 group-hover:bg-primary-container transition-colors">
                <span class="material-symbols-outlined text-primary text-3xl">description</span>
              </div>
              <div class="mb-2 text-primary font-bold text-sm">Langkah 3</div>
              <h3 class="font-headline-sm text-lg font-bold mb-2">Hasil Diagnosa</h3>
              <p class="font-body-sm text-body-sm text-on-surface-variant">Dapatkan laporan diagnosis lengkap beserta tingkat probabilitas dan rekomendasi tindakan klinis awal.</p>
            </div>
          </div>
        </div>
      </section>

      <!-- Why Choose Us (Asymmetric Layout) -->
      <section id="tentang-kami" class="py-16 bg-surface relative overflow-hidden">
        <div class="container mx-auto px-6 md:px-8 grid md:grid-cols-2 gap-12 items-center">
          <div class="order-2 md:order-1 relative">
            <div class="aspect-square bg-primary-container/20 rounded-3xl overflow-hidden relative group">
              <img class="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110" src="https://lh3.googleusercontent.com/aida-public/AB6AXuBy_s9D1PeTovrhAPQ019c9Hw0uIuP3Zwrois3pTTEu_E8bF_yV5I1RHPjM9EZCgQHs8p3q4SU_yNr_6CFrb7Dy_zaDTrBrlV1eAa1z_EVRSV76J3Kuv3imuoFqKZj6N81yFX6qojlRETO43K8yRudzXw1DoYgz6KaW6PvqLPjyrPf587cDD-U1T-7Ac_bp-1_WIVwvB2dioGNY9q39m7k-YIS2hhscY05FHdaO7kQsw6tqavta3gG7t9kdZOnMeYEsh0sL_MGCplZv"/>
              <div class="absolute bottom-6 left-6 glass-card p-4 rounded-xl flex items-center gap-3">
                <div class="w-12 h-12 bg-primary rounded-full flex items-center justify-center text-on-primary">
                  <span class="material-symbols-outlined">verified_user</span>
                </div>
                <div>
                  <div class="font-label-md text-xs font-bold">Terverifikasi</div>
                  <div class="font-body-sm text-xs text-on-surface-variant">Standar Medis Internasional</div>
                </div>
              </div>
            </div>
          </div>

          <div class="order-1 md:order-2 flex flex-col gap-6">
            <h2 id="metodologi" class="font-headline-lg text-3xl font-bold text-on-surface">Mengapa Memilih ENT Expert?</h2>
            <p class="font-body-md text-body-md text-on-surface-variant">Kami menggabungkan keahlian klinis dengan teknologi AI terbaru untuk memberikan pengalaman diagnostik terbaik.</p>

            <div class="space-y-4">
              <div class="flex gap-4">
                <span class="material-symbols-outlined text-primary" style="font-variation-settings: 'FILL' 1;">check_circle</span>
                <div>
                  <h4 class="font-headline-sm text-sm font-bold text-on-surface">Akurasi Tinggi</h4>
                  <p class="font-body-sm text-xs text-on-surface-variant leading-relaxed">Model statistik yang divalidasi oleh dokter spesialis senior untuk akurasi optimal.</p>
                </div>
              </div>

              <div class="flex gap-4">
                <span class="material-symbols-outlined text-primary" style="font-variation-settings: 'FILL' 1;">lock</span>
                <div>
                  <h4 class="font-headline-sm text-sm font-bold text-on-surface">Privasi Terjamin</h4>
                  <p class="font-body-sm text-xs text-on-surface-variant leading-relaxed">Enkripsi data tingkat tinggi memastikan riwayat medis pasien tetap aman dan rahasia.</p>
                </div>
              </div>

              <div class="flex gap-4">
                <span class="material-symbols-outlined text-primary" style="font-variation-settings: 'FILL' 1;">support_agent</span>
                <div>
                  <h4 class="font-headline-sm text-sm font-bold text-on-surface">Dukungan Klinis</h4>
                  <p class="font-body-sm text-xs text-on-surface-variant leading-relaxed">Integrasi mudah dengan sistem manajemen rumah sakit dan rekam medis elektronik.</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Final CTA -->
      <section class="py-16">
        <div class="container mx-auto px-6 md:px-8">
          <div class="bg-primary-container rounded-[2rem] p-8 md:p-12 text-center flex flex-col items-center gap-6 overflow-hidden relative">
            <div class="absolute top-0 left-0 w-64 h-64 bg-white/10 rounded-full blur-3xl -translate-x-1/2 -translate-y-1/2"></div>
            <div class="absolute bottom-0 right-0 w-96 h-96 bg-white/5 rounded-full blur-3xl translate-x-1/4 translate-y-1/4"></div>

            <h2 class="font-display text-2xl md:text-3xl font-bold text-on-primary-container max-w-3xl">
              Siap Meningkatkan Kualitas Layanan Kesehatan Anda?
            </h2>

            <p class="font-body-lg text-body-lg text-on-primary-container/80 max-w-2xl">
              Bergabunglah dengan ribuan profesional medis lainnya dalam mendigitalkan diagnosis THT.
            </p>

            <div class="flex flex-col sm:flex-row gap-4 mt-2">
              <router-link to="/register" class="bg-[#ffffff] text-primary-container px-6 py-3 rounded-xl font-headline-sm text-sm font-bold hover:bg-surface transition-colors shadow-lg">
                Daftar Sekarang
              </router-link>
              <router-link to="/login" class="border border-on-primary-container text-on-primary-container px-6 py-3 rounded-xl font-headline-sm text-sm font-bold hover:bg-on-primary-container/10 transition-colors">
                Masuk Portal
              </router-link>
            </div>
          </div>
        </div>
      </section>
    </main>

    <!-- Footer -->
    <footer class="w-full py-8 px-6 md:px-8 flex flex-col md:flex-row justify-between items-start md:items-center gap-6 bg-surface-container border-t border-outline-variant/20 mt-12 shrink-0">
      <div class="flex flex-col gap-2">
        <div class="flex items-center gap-2">
          <span class="material-symbols-outlined text-primary text-xl" style="font-variation-settings: 'FILL' 1;">stethoscope</span>
          <span class="font-headline-sm text-sm font-bold text-primary">ENT Expert</span>
        </div>
        <p class="font-body-sm text-xs text-on-surface-variant max-w-xs leading-relaxed">
          Solusi klinis masa depan untuk diagnosa THT yang lebih presisi dan efisien.
        </p>
        <p class="font-body-sm text-[11px] text-on-surface-variant mt-4">
          © 2026 ENT Expert Medical Systems. All rights reserved.
        </p>
      </div>

      <div class="grid grid-cols-3 gap-8">
        <div class="flex flex-col gap-1.5">
          <span class="font-label-md text-xs text-on-surface font-bold uppercase tracking-wider">Produk</span>
          <a class="font-body-sm text-xs text-on-surface-variant hover:text-primary transition-colors" href="#">Fitur Utama</a>
          <a class="font-body-sm text-xs text-on-surface-variant hover:text-primary transition-colors" href="#">Integrasi</a>
        </div>
        <div class="flex flex-col gap-1.5">
          <span class="font-label-md text-xs text-on-surface font-bold uppercase tracking-wider">Perusahaan</span>
          <a class="font-body-sm text-xs text-on-surface-variant hover:text-primary transition-colors" href="#">Tentang Kami</a>
          <a class="font-body-sm text-xs text-on-surface-variant hover:text-primary transition-colors" href="#">Metodologi</a>
        </div>
        <div class="flex flex-col gap-1.5">
          <span class="font-label-md text-xs text-on-surface font-bold uppercase tracking-wider">Bantuan</span>
          <a class="font-body-sm text-xs text-on-surface-variant hover:text-primary transition-colors" href="#">Pusat Bantuan</a>
          <a class="font-body-sm text-xs text-on-surface-variant hover:text-primary transition-colors" href="#">Privasi</a>
        </div>
      </div>
    </footer>

  </div>
</template>

<script setup>
// Landing page uses standard routes for navigation. No extra script setup required.
</script>

<style scoped>
.glass-card {
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(226, 232, 240, 0.8);
}
</style>
