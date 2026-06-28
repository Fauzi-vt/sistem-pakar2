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
            <h1 class="font-headline-sm text-headline-sm font-bold text-primary truncate leading-tight">Pengaturan Sistem</h1>
            <p class="text-xs text-on-surface-variant hidden sm:block mt-0.5">Konfigurasi preferensi klinis dan basis data</p>
          </div>
        </div>
      </header>

      <!-- Main Canvas -->
      <main class="p-container-padding flex-1 flex flex-col gap-stack-lg">
        
        <!-- Setting Panels -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-gutter">
          
          <!-- Clinic Info Card -->
          <div class="bg-surface-container-lowest border border-outline-variant rounded p-6 shadow-sm flex flex-col gap-4">
            <div>
              <h3 class="font-body-md font-bold text-primary">Informasi Instansi Medis</h3>
              <p class="text-xs text-on-surface-variant">Detail institusi klinik yang dicantumkan pada diagnosa</p>
            </div>

            <div class="space-y-3">
              <div>
                <label class="block text-xs font-bold text-on-surface-variant mb-1">Nama Rumah Sakit / Klinik</label>
                <input type="text" v-model="clinicName" class="w-full bg-surface-container-lowest border border-outline-variant rounded px-3 py-2 text-sm text-on-surface focus:border-secondary focus:ring-1 focus:ring-secondary outline-none transition-all"/>
              </div>
              <div>
                <label class="block text-xs font-bold text-on-surface-variant mb-1">Alamat Klinik</label>
                <textarea rows="2" v-model="clinicAddress" class="w-full bg-surface-container-lowest border border-outline-variant rounded px-3 py-2 text-sm text-on-surface focus:border-secondary focus:ring-1 focus:ring-secondary outline-none transition-all resize-none"></textarea>
              </div>
            </div>

            <button @click="saveClinicInfo" class="mt-2 self-start bg-primary text-on-tertiary font-bold text-xs py-2 px-4 rounded hover:bg-primary-container cursor-pointer transition-all active:scale-95">
              Simpan Informasi
            </button>
          </div>

          <!-- Database Administration Card -->
          <div class="bg-surface-container-lowest border border-outline-variant rounded p-6 shadow-sm flex flex-col gap-4">
            <div>
              <h3 class="font-body-md font-bold text-primary">Utilitas Basis Data</h3>
              <p class="text-xs text-on-surface-variant">Tindakan pemeliharaan dan pengisian data master</p>
            </div>

            <div class="p-4 bg-surface rounded border border-outline-variant/60 flex flex-col gap-2">
              <h4 class="text-xs font-bold text-primary flex items-center gap-1.5">
                <span class="material-symbols-outlined text-[16px] text-secondary">database</span>
                Seeding Data Master
              </h4>
              <p class="text-xs text-on-surface-variant leading-relaxed">
                Menyuntikkan set data master penyakit dan gejala THT awal untuk mempercepat konfigurasi sistem pertama kali.
              </p>
              
              <button @click="triggerSeeding" :disabled="seeding"
                      class="mt-2 self-start bg-secondary text-on-tertiary font-bold text-xs py-2 px-4 rounded hover:bg-[#0d595a] disabled:opacity-50 transition-all cursor-pointer flex items-center gap-2">
                <span v-if="seeding" class="w-3 h-3 border-2 border-white border-t-transparent rounded-full animate-spin"></span>
                <span>Jalankan Seeding</span>
              </button>
            </div>
          </div>

        </div>

      </main>

      <!-- Footer -->
      <footer class="border-t border-outline-variant px-6 py-4 bg-surface-container-lowest shrink-0">
        <p class="text-on-surface-variant text-xs text-center">© 2026 Sistem Pakar THT — Kelompok 2 · RS Jasa Kartini. All rights reserved.</p>
      </footer>
    </div>

    <!-- ── TOAST NOTIFICATIONS ── -->
    <div class="fixed bottom-6 right-6 z-50 flex flex-col gap-2.5 max-w-sm w-full">
      <TransitionGroup name="toast-list">
        <div v-for="toast in toasts" :key="toast.id" class="flex items-start gap-3 p-4 bg-surface-container-lowest rounded-xl border shadow-2xl transition-all duration-300 border-outline-variant/60">
          <div class="mt-0.5 shrink-0">
            <span v-if="toast.type === 'success'" class="material-symbols-outlined text-secondary">check_circle</span>
            <span v-else class="material-symbols-outlined text-error">error</span>
          </div>
          <div class="flex-1">
            <p class="text-sm font-bold leading-tight text-primary">{{ toast.type === 'success' ? 'Sukses' : 'Gagal' }}</p>
            <p class="text-xs mt-0.5 leading-relaxed text-on-surface-variant">{{ toast.message }}</p>
          </div>
          <button @click="removeToast(toast.id)" class="text-on-surface-variant hover:text-on-surface cursor-pointer shrink-0">
            <span class="material-symbols-outlined text-base">close</span>
          </button>
        </div>
      </TransitionGroup>
    </div>

  </div>
</template>

<script setup>
import { ref } from 'vue'
import Sidebar from '../../components/Sidebar.vue'

const sidebarOpen = ref(false)

const clinicName = ref('RS Jasa Kartini')
const clinicAddress = ref('Jl. Siliwangi No. 189, Tasikmalaya, Jawa Barat')

const seeding = ref(false)

const toasts = ref([])
let toastIdCounter = 0

const showToast = (type, message) => {
  const id = toastIdCounter++
  toasts.value.push({ id, type, message })
  setTimeout(() => removeToast(id), 4500)
}
const removeToast = (id) => { toasts.value = toasts.value.filter(t => t.id !== id) }

const saveClinicInfo = () => {
  showToast('success', 'Informasi instansi medis berhasil disimpan.')
}

const triggerSeeding = async () => {
  seeding.value = true
  try {
    const res = await fetch('http://127.0.0.1:8000/api/seed-master-data', { method: 'POST' }).then(r => r.json())
    if (res.success) {
      showToast('success', `Seeding sukses! Berhasil mendaftarkan ${res.summary.penyakit_seeded} penyakit dan ${res.summary.gejala_seeded} gejala.`)
    } else {
      showToast('error', 'Gagal seeding: ' + (res.errors.join(', ')))
    }
  } catch (err) {
    showToast('error', 'Gagal memanggil API seeding: ' + err.message)
  } finally {
    seeding.value = false
  }
}
</script>

<style scoped>
.toast-list-enter-active { transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275); }
.toast-list-leave-active { transition: all 0.2s ease-in; position: absolute; }
.toast-list-enter-from   { transform: translateY(20px) scale(0.9); opacity: 0; }
.toast-list-leave-to     { transform: translateX(100px); opacity: 0; }
</style>
