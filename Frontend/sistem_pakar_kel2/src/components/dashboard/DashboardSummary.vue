<template>
  <section>
    <h2 class="font-headline-md text-headline-md text-primary mb-stack-md">Dashboard Overview</h2>
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-gutter">
      
      <!-- Metric Card 1: Total Penyakit -->
      <div class="bg-surface-container-lowest border border-outline-variant rounded p-stack-md flex flex-col gap-stack-sm hover:shadow-[0_4px_12px_rgba(26,54,93,0.05)] transition-shadow">
        <div class="flex justify-between items-center text-on-surface-variant">
          <span class="font-label-sm text-label-sm uppercase tracking-wider">Total Penyakit</span>
          <Stethoscope class="w-5 h-5 text-on-surface-variant" />
        </div>
        <div class="font-headline-lg text-headline-lg text-primary">{{ stats.total_penyakit }}</div>
        <div class="font-body-sm text-body-sm text-secondary flex items-center gap-1">
          <ArrowUp class="w-4 h-4 text-secondary" />
          <span>+2 bulan ini</span>
        </div>
      </div>

      <!-- Metric Card 2: Basis Aturan -->
      <div class="bg-surface-container-lowest border border-outline-variant rounded p-stack-md flex flex-col gap-stack-sm hover:shadow-[0_4px_12px_rgba(26,54,93,0.05)] transition-shadow">
        <div class="flex justify-between items-center text-on-surface-variant">
          <span class="font-label-sm text-label-sm uppercase tracking-wider">Basis Aturan</span>
          <BookOpen class="w-5 h-5 text-on-surface-variant" />
        </div>
        <div class="font-headline-lg text-headline-lg text-primary">{{ stats.total_aturan }}</div>
        <div class="font-body-sm text-body-sm text-secondary flex items-center gap-1">
          <CheckCircle class="w-4 h-4 text-secondary" />
          <span>Tersinkronisasi</span>
        </div>
      </div>

      <!-- Metric Card 3: Total Gejala -->
      <div class="bg-surface-container-lowest border border-outline-variant rounded p-stack-md flex flex-col gap-stack-sm hover:shadow-[0_4px_12px_rgba(26,54,93,0.05)] transition-shadow">
        <div class="flex justify-between items-center text-on-surface-variant">
          <span class="font-label-sm text-label-sm uppercase tracking-wider">Total Gejala</span>
          <Activity class="w-5 h-5 text-on-surface-variant" />
        </div>
        <div class="font-headline-lg text-headline-lg text-primary">{{ stats.total_gejala }}</div>
        <div class="font-body-sm text-body-sm text-on-surface-variant flex items-center gap-1">
          <span>Menunggu validasi</span>
        </div>
      </div>

      <!-- Metric Card 4: Pasien Terdiagnosa -->
      <div class="bg-surface-container-lowest border border-outline-variant rounded p-stack-md flex flex-col gap-stack-sm hover:shadow-[0_4px_12px_rgba(26,54,93,0.05)] transition-shadow">
        <div class="flex justify-between items-center text-on-surface-variant">
          <span class="font-label-sm text-label-sm uppercase tracking-wider">Pasien Terdiagnosa</span>
          <Users class="w-5 h-5 text-on-surface-variant" />
        </div>
        <div class="font-headline-lg text-headline-lg text-primary">{{ stats.total_riwayat }}</div>
        <div class="font-body-sm text-body-sm text-secondary flex items-center gap-1">
          <TrendingUp class="w-4 h-4 text-secondary" />
          <span>+12% vs pekan lalu</span>
        </div>
      </div>

    </div>
  </section>
</template>

<script setup>
import { Stethoscope, BookOpen, Activity, Users, ArrowUp, TrendingUp, CheckCircle } from 'lucide-vue-next'

defineProps({
  stats: {
    type: Object,
    required: true,
    default: () => ({ total_penyakit: 0, total_aturan: 0, total_gejala: 0, total_riwayat: 0 })
  }
})
</script>
