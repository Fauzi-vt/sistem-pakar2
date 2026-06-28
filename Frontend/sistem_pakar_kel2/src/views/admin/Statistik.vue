<template>
  <div class="min-h-screen bg-background text-on-background font-body-md flex relative antialiased">
    <!-- Side Navigation -->
    <Sidebar v-model:isOpen="sidebarOpen" />

    <!-- Main Content Area -->
    <div class="flex-1 flex flex-col min-h-screen lg:ml-64 transition-all duration-300">
      
      <!-- Top Navigation Header -->
      <header class="bg-surface-container-lowest dark:bg-surface-container flex justify-between items-center w-full px-container-padding h-16 sticky top-0 z-40 border-b border-outline-variant">
        <div class="flex items-center gap-4 w-full lg:w-1/2">
          <button @click="sidebarOpen = !sidebarOpen" 
                  class="lg:hidden flex items-center justify-center p-2 bg-surface-container rounded-lg text-on-surface hover:bg-surface-container-high transition-colors">
            <span class="material-symbols-outlined">menu</span>
          </button>
          <div>
            <h1 class="font-headline-sm text-headline-sm font-bold text-primary truncate leading-tight">Statistik Diagnosa</h1>
            <p class="text-xs text-on-surface-variant hidden sm:block mt-0.5">Analisis hasil pemeriksaan klinis Bayes</p>
          </div>
        </div>
      </header>

      <!-- Main Canvas -->
      <main class="p-container-padding flex-1 flex flex-col gap-stack-lg">
        
        <!-- Metrics overview -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-gutter">
          
          <!-- Disease Distribution Chart Card -->
          <div class="bg-surface-container-lowest border border-outline-variant rounded p-6 shadow-sm flex flex-col gap-4">
            <div>
              <h3 class="font-body-md font-bold text-primary">Distribusi Diagnosis Terbanyak</h3>
              <p class="text-xs text-on-surface-variant">Frekuensi relatif hasil pemeriksaan pasien</p>
            </div>
            
            <div class="space-y-4 py-2">
              <div v-for="d in diseaseChartData" :key="d.name" class="space-y-1.5">
                <div class="flex justify-between items-center text-xs font-semibold">
                  <span class="text-primary">{{ d.name }}</span>
                  <span class="text-on-surface-variant font-bold">{{ d.count }} kasus ({{ d.pct }}%)</span>
                </div>
                <div class="w-full bg-surface-container rounded-full h-2.5 overflow-hidden">
                  <div class="bg-primary h-2.5 rounded-full" :style="{ width: `${d.pct}%` }"></div>
                </div>
              </div>
            </div>
          </div>

          <!-- Score Distribution Card -->
          <div class="bg-surface-container-lowest border border-outline-variant rounded p-6 shadow-sm flex flex-col gap-4">
            <div>
              <h3 class="font-body-md font-bold text-primary">Tingkat Keyakinan Inferensi</h3>
              <p class="text-xs text-on-surface-variant">Distribusi persentase keyakinan Bayes</p>
            </div>
            
            <div class="space-y-4 py-2">
              <div v-for="s in scoreChartData" :key="s.range" class="space-y-1.5">
                <div class="flex justify-between items-center text-xs font-semibold">
                  <span class="text-primary">{{ s.range }}</span>
                  <span class="text-on-surface-variant font-bold">{{ s.count }} pasien</span>
                </div>
                <div class="w-full bg-surface-container rounded-full h-2.5 overflow-hidden">
                  <div class="bg-secondary h-2.5 rounded-full" :style="{ width: `${s.pct}%` }"></div>
                </div>
              </div>
            </div>
          </div>

        </div>

      </main>

      <!-- Footer -->
      <footer class="border-t border-outline-variant px-6 py-4 bg-surface-container-lowest shrink-0">
        <p class="text-on-surface-variant text-xs text-center">© 2026 Sistem Pakar THT — Kelompok 2 · RS Jasa Kartini. All rights reserved.</p>
      </footer>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import Sidebar from '../../components/Sidebar.vue'

const sidebarOpen = ref(false)

// Simulated clinical distribution data
const diseaseChartData = ref([
  { name: 'Tonsilitis', count: 18, pct: 42 },
  { name: 'Rhinitis Alergi', count: 14, pct: 33 },
  { name: 'Otitis Externa', count: 10, pct: 25 }
])

const scoreChartData = ref([
  { range: '>= 80% (Tinggi)', count: 24, pct: 57 },
  { range: '50% - 79% (Sedang)', count: 13, pct: 31 },
  { range: '< 50% (Rendah)', count: 5, pct: 12 }
])
</script>
