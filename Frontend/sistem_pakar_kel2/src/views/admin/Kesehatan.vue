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
            <h1 class="font-headline-sm text-headline-sm font-bold text-primary truncate leading-tight">Status Kesehatan Sistem</h1>
            <p class="text-xs text-on-surface-variant hidden sm:block mt-0.5">Pantau kesehatan infrastruktur server dan database</p>
          </div>
        </div>
      </header>

      <!-- Main Canvas -->
      <main class="p-container-padding flex-1 flex flex-col gap-stack-lg">
        
        <!-- Metrics Grid -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-gutter">
          <!-- Database Status -->
          <div class="bg-surface-container-lowest border border-outline-variant rounded p-stack-md flex flex-col gap-2 shadow-sm">
            <div class="flex justify-between items-center text-on-surface-variant">
              <span class="font-label-sm text-label-sm uppercase tracking-wider">Koneksi Database</span>
              <span class="w-3 h-3 rounded-full bg-emerald-500 animate-pulse"></span>
            </div>
            <div class="font-headline-sm text-headline-sm text-primary font-bold">Terhubung</div>
            <p class="text-xs text-on-surface-variant">Supabase API terintegrasi penuh.</p>
          </div>

          <!-- Server Latency -->
          <div class="bg-surface-container-lowest border border-outline-variant rounded p-stack-md flex flex-col gap-2 shadow-sm">
            <div class="flex justify-between items-center text-on-surface-variant">
              <span class="font-label-sm text-label-sm uppercase tracking-wider">Latensi API</span>
              <span class="material-symbols-outlined text-[18px] text-secondary">speed</span>
            </div>
            <div class="font-headline-sm text-headline-sm text-primary font-bold">14 ms</div>
            <p class="text-xs text-on-surface-variant">Respons server di bawah ambang batas kritis.</p>
          </div>

          <!-- Environment -->
          <div class="bg-surface-container-lowest border border-outline-variant rounded p-stack-md flex flex-col gap-2 shadow-sm">
            <div class="flex justify-between items-center text-on-surface-variant">
              <span class="font-label-sm text-label-sm uppercase tracking-wider">Environment Mode</span>
              <span class="material-symbols-outlined text-[18px] text-primary">terminal</span>
            </div>
            <div class="font-headline-sm text-headline-sm text-primary font-bold">Production</div>
            <p class="text-xs text-on-surface-variant">Konfigurasi build optimal terpasang.</p>
          </div>
        </div>

        <!-- Logs section -->
        <section class="bg-surface-container-lowest border border-outline-variant rounded p-6 shadow-sm flex flex-col gap-4">
          <div>
            <h3 class="font-body-md font-bold text-primary">Log Aktivitas Sistem</h3>
            <p class="text-xs text-on-surface-variant">Daftar operasi sistem klinis terbaru</p>
          </div>

          <div class="bg-background rounded border border-outline-variant/60 p-4 font-mono text-xs text-on-surface space-y-2 h-72 overflow-y-auto">
            <div class="flex gap-4"><span class="text-secondary shrink-0">[16:52:10]</span><span class="text-primary font-semibold">INFO:</span><span>Database connection check successful. (0 errors)</span></div>
            <div class="flex gap-4"><span class="text-secondary shrink-0">[16:47:04]</span><span class="text-primary font-semibold">INFO:</span><span>Seed script master data initialized check done.</span></div>
            <div class="flex gap-4"><span class="text-secondary shrink-0">[16:44:56]</span><span class="text-primary font-semibold">INFO:</span><span>Aturan probabilitas kondisional Teorema Bayes sync triggered.</span></div>
            <div class="flex gap-4"><span class="text-secondary shrink-0">[16:12:35]</span><span class="text-primary font-semibold">INFO:</span><span>Supabase client connection created successfully.</span></div>
            <div class="flex gap-4"><span class="text-secondary shrink-0">[15:30:12]</span><span class="text-primary font-semibold">INFO:</span><span>FastAPI engine reload completed. Server running on port 8000.</span></div>
          </div>
        </section>

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
</script>
