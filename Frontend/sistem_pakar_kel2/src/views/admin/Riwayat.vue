<template>
  <div class="min-h-screen bg-background text-on-background font-body-md flex relative antialiased">
    <!-- Side Navigation -->
    <Sidebar v-model:isOpen="sidebarOpen" />

    <!-- Main Content Area -->
    <div class="flex-1 flex flex-col min-h-screen lg:ml-64 transition-all duration-300">
      
      <!-- Top Navigation Header -->
      <header class="bg-surface-container-lowest dark:bg-surface-container flex justify-between items-center w-full px-container-padding h-16 sticky top-0 z-40 border-b border-outline-variant">
        <!-- Left: Search and Toggle -->
        <div class="flex items-center gap-4 w-full lg:w-1/3">
          <button @click="sidebarOpen = !sidebarOpen" 
                  class="lg:hidden flex items-center justify-center p-2 bg-surface-container rounded-lg text-on-surface hover:bg-surface-container-high transition-colors">
            <span class="material-symbols-outlined">menu</span>
          </button>
          <div class="relative w-full hidden sm:block">
            <span class="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-on-surface-variant">search</span>
            <input 
              v-model="searchQuery"
              @input="currentPage = 1"
              class="w-full bg-surface-container-lowest border border-outline-variant rounded pl-10 pr-4 py-2 font-body-sm text-on-surface focus:border-secondary focus:ring-1 focus:ring-secondary outline-none transition-all" 
              placeholder="Cari nama atau hasil diagnosa..." 
              type="text"
            >
          </div>
        </div>

        <!-- Right User Profile Pic -->
        <div class="flex items-center gap-stack-md">
          <div class="w-8 h-8 rounded-full overflow-hidden border border-outline-variant">
            <img alt="Medical professional" class="w-full h-full object-cover" src="https://lh3.googleusercontent.com/aida-public/AB6AXuAWoTwRpq8rwHSTU8reRlgKRBb7Tf8kV8t1VUE4fvM26yNC6MXOhO6Tm1gNontoTHWXYVG6snsrEbPirYlDmEubo5uVWTDUg-zGhfC0aFJ64DrphSP--FKm8rikvYkNwbnZMz3jy5cnmviRio9u8k7foQY8i0tCTdBSTZgP9PqFjjXuWTzR-x3e_5md1hzOECJNB2qysMU_IJc4ECf6-CGkDL-NxOA2_Vt4VTJ003gjVOYTziW7T9M-lD4Qwypg4MSCStzTXpRYhFkl">
          </div>
        </div>
      </header>

      <!-- Main Canvas -->
      <main class="p-container-padding flex-1 flex flex-col gap-stack-lg">
        
        <!-- Page Title -->
        <div>
          <h2 class="font-headline-md text-headline-md text-primary">Riwayat Diagnosa Pasien</h2>
          <p class="font-body-sm text-body-sm text-on-surface-variant mt-1">Kelola dan tinjau log hasil pemeriksaan klinis pasien THT.</p>
        </div>

        <!-- Overview stats -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-gutter">
          <div class="bg-surface-container-lowest border border-outline-variant rounded p-stack-md hover:shadow-[0_4px_12px_rgba(26,54,93,0.02)] transition-all">
            <span class="font-label-sm text-label-sm uppercase tracking-wider text-on-surface-variant block mb-1">Total Pemeriksaan</span>
            <div class="font-headline-lg text-headline-lg text-primary">{{ riwayatList.length }}</div>
          </div>
          <div class="bg-surface-container-lowest border border-outline-variant rounded p-stack-md hover:shadow-[0_4px_12px_rgba(26,54,93,0.02)] transition-all">
            <span class="font-label-sm text-label-sm uppercase tracking-wider text-on-surface-variant block mb-1">Diagnosis Mayoritas</span>
            <div class="font-body-md font-bold text-primary mt-1 truncate">{{ topDiagnosisName }}</div>
          </div>
        </div>

        <!-- Table Card -->
        <section class="bg-surface-container-lowest border border-outline-variant rounded flex flex-col shadow-sm">
          <div class="overflow-x-auto">
            <table class="w-full text-left border-collapse">
              <thead>
                <tr class="border-b border-primary bg-background">
                  <th class="p-4 pl-6 font-label-sm text-label-sm text-on-surface-variant uppercase tracking-wider">Tanggal</th>
                  <th class="p-4 font-label-sm text-label-sm text-on-surface-variant uppercase tracking-wider">Nama Pasien</th>
                  <th class="p-4 font-label-sm text-label-sm text-on-surface-variant uppercase tracking-wider">Hasil Diagnosis</th>
                  <th class="p-4 font-label-sm text-label-sm text-on-surface-variant uppercase tracking-wider">Gejala Terpilih</th>
                  <th class="p-4 font-label-sm text-label-sm text-on-surface-variant uppercase tracking-wider">Nilai Bayes</th>
                  <th class="p-4 pr-6 font-label-sm text-label-sm text-on-surface-variant uppercase tracking-wider text-right">Aksi</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-outline-variant/30">
                <tr v-if="loading">
                  <td colspan="6" class="p-12 text-center text-on-surface-variant">
                    <div class="flex items-center justify-center gap-2">
                      <span class="w-4 h-4 border-2 border-t-transparent rounded-full animate-spin border-primary"></span>
                      <span>Memuat data riwayat...</span>
                    </div>
                  </td>
                </tr>
                <tr v-else-if="filteredRiwayat.length === 0">
                  <td colspan="6" class="p-12 text-center text-on-surface-variant italic">Tidak ada data riwayat diagnosa</td>
                </tr>
                
                <tr v-else v-for="item in paginatedRiwayat" :key="item.id"
                    class="bg-surface-container-lowest hover:bg-surface-container-low transition-colors group">
                  <!-- Tanggal -->
                  <td class="p-4 pl-6 text-on-surface-variant font-label-sm text-xs">
                    {{ formatDate(item.tanggal) }}
                  </td>
                  
                  <!-- Nama -->
                  <td class="p-4 font-bold text-primary">
                    {{ item.name }}
                  </td>
                  
                  <!-- Hasil -->
                  <td class="p-4 font-body-sm text-on-surface font-semibold">
                    {{ item.diagnosis }}
                  </td>

                  <!-- Gejala -->
                  <td class="p-4 text-xs text-on-surface-variant">
                    {{ item.symptoms_count }} Gejala terpilih
                  </td>

                  <!-- Bayes Percentage -->
                  <td class="p-4">
                    <span class="px-2.5 py-1 rounded-full text-xs font-bold border" :class="getBadgeCls(item.percentage)">
                      {{ (item.percentage * 100).toFixed(1) }}%
                    </span>
                  </td>
                  
                  <!-- Aksi -->
                  <td class="p-4 pr-6 text-right">
                    <div class="flex items-center justify-end gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                      <button @click="viewDetail(item)"
                              class="text-secondary hover:text-primary p-1.5 rounded hover:bg-surface-container-high transition-colors cursor-pointer"
                              title="Detail Diagnosa">
                        <span class="material-symbols-outlined text-[20px]">visibility</span>
                      </button>
                      <button @click="confirmDelete(item)"
                              class="text-error hover:bg-error-container rounded p-1.5 transition-colors cursor-pointer"
                              title="Hapus Record">
                        <span class="material-symbols-outlined text-[20px]">delete</span>
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Pagination Footer -->
          <div v-if="filteredRiwayat.length > 0" 
               class="p-4 border-t border-outline-variant/50 flex flex-col sm:flex-row items-center justify-between gap-4">
            <span class="font-body-sm text-body-sm text-on-surface-variant">
              Menampilkan {{ pageStartIndex }}-{{ pageEndIndex }} dari {{ filteredRiwayat.length }} riwayat
            </span>
            <div class="flex items-center gap-1">
              <button @click="currentPage > 1 && currentPage--" 
                      :disabled="currentPage === 1"
                      class="w-8 h-8 rounded border border-outline-variant flex items-center justify-center hover:bg-surface-container-low cursor-pointer disabled:opacity-40 disabled:cursor-not-allowed text-on-surface">
                <span class="material-symbols-outlined text-base">chevron_left</span>
              </button>
              
              <button v-for="page in totalPages" :key="page"
                      @click="currentPage = page"
                      class="w-8 h-8 rounded text-sm font-semibold flex items-center justify-center transition-colors cursor-pointer"
                      :class="currentPage === page 
                        ? 'bg-primary text-on-tertiary font-bold' 
                        : 'border border-outline-variant text-on-surface hover:bg-surface-container-low'">
                {{ page }}
              </button>

              <button @click="currentPage < totalPages && currentPage++" 
                      :disabled="currentPage === totalPages"
                      class="w-8 h-8 rounded border border-outline-variant flex items-center justify-center hover:bg-surface-container-low cursor-pointer disabled:opacity-40 disabled:cursor-not-allowed text-on-surface">
                <span class="material-symbols-outlined text-base">chevron_right</span>
              </button>
            </div>
          </div>
        </section>

      </main>

      <!-- Footer -->
      <footer class="border-t border-outline-variant px-6 py-4 bg-surface-container-lowest shrink-0">
        <p class="text-on-surface-variant text-xs text-center">© 2026 Sistem Pakar THT — Kelompok 2 · RS Jasa Kartini. All rights reserved.</p>
      </footer>
    </div>

    <!-- ── DETAIL MODAL ── -->
    <Transition name="modal-fade">
      <div v-if="detailOpen" class="fixed inset-0 z-50 flex items-center justify-center p-4">
        <!-- Overlay -->
        <div @click="detailOpen = false" class="absolute inset-0 bg-inverse-surface/60 backdrop-blur-sm"></div>

        <!-- Dialog Box -->
        <div class="relative w-full max-w-lg bg-surface-container-lowest rounded-xl shadow-2xl overflow-hidden border border-outline-variant animate-modal-pop">
          <div class="px-6 py-4 border-b border-outline-variant bg-surface-container-low flex items-center justify-between">
            <h3 class="font-bold text-primary flex items-center gap-2">
              <span class="material-symbols-outlined text-[20px] text-secondary">info</span>
              Rincian Diagnosa Klinis
            </h3>
            <button @click="detailOpen = false" class="text-on-surface-variant hover:text-on-surface cursor-pointer">
              <span class="material-symbols-outlined text-lg">close</span>
            </button>
          </div>

          <div class="p-6 space-y-4 text-sm leading-relaxed" v-if="selectedItem">
            <div>
              <span class="text-xs uppercase font-bold tracking-wider text-on-surface-variant block">Nama Pasien</span>
              <p class="font-bold text-primary text-base">{{ selectedItem.name }}</p>
            </div>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <span class="text-xs uppercase font-bold tracking-wider text-on-surface-variant block">Tanggal Pemeriksaan</span>
                <p class="font-medium text-on-surface text-xs">{{ formatDate(selectedItem.tanggal) }}</p>
              </div>
              <div>
                <span class="text-xs uppercase font-bold tracking-wider text-on-surface-variant block">Keyakinan Bayes</span>
                <p class="font-bold text-secondary text-sm">{{ (selectedItem.percentage * 100).toFixed(2) }}%</p>
              </div>
            </div>
            <div>
              <span class="text-xs uppercase font-bold tracking-wider text-on-surface-variant block">Hasil Diagnosis Akhir</span>
              <div class="p-3 bg-secondary-container text-on-secondary-container rounded-lg border border-secondary/20 font-bold">
                {{ selectedItem.diagnosis }}
              </div>
            </div>
            <div>
              <span class="text-xs uppercase font-bold tracking-wider text-on-surface-variant block mb-1">Daftar Gejala Terdeteksi</span>
              <div class="flex flex-wrap gap-1.5">
                <span v-for="gid in selectedItem.gejala_ids" :key="gid" 
                      class="px-2 py-1 bg-surface-container border border-outline-variant/60 rounded text-xs text-primary font-semibold">
                  {{ gid }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Transition>

    <!-- ── CONFIRM DELETE MODAL ── -->
    <Transition name="modal-fade">
      <div v-if="deleteModalOpen" class="fixed inset-0 z-50 flex items-center justify-center p-4">
        <!-- Overlay -->
        <div @click="closeDeleteModal" class="absolute inset-0 bg-inverse-surface/60 backdrop-blur-sm"></div>

        <!-- Dialog Box -->
        <div class="relative w-full max-w-md bg-surface-container-lowest rounded-xl shadow-2xl overflow-hidden border border-outline-variant animate-modal-pop">
          <div class="p-6 text-center">
            <div class="w-14 h-14 rounded-full bg-error-container text-on-error-container flex items-center justify-center mx-auto mb-4 border border-error/20">
              <span class="material-symbols-outlined text-2xl text-error">delete</span>
            </div>

            <h3 class="font-bold text-lg mb-2 text-primary">Hapus Record?</h3>
            <p class="text-sm mb-6 leading-relaxed text-on-surface-variant">
              Apakah Anda yakin ingin menghapus record diagnosa <strong class="text-primary">{{ itemToDelete?.name }} - {{ itemToDelete?.diagnosis }}</strong>?
              <br><span class="text-xs mt-1 block text-error font-semibold">Tindakan ini permanen dan tidak dapat dibatalkan.</span>
            </p>

            <div class="flex items-center justify-center gap-3">
              <button @click="closeDeleteModal" class="px-4 py-2 border border-outline-variant rounded font-semibold hover:bg-surface-container-low transition-colors cursor-pointer text-on-surface">
                Batal
              </button>
              <button @click="handleDelete" :disabled="submitting" class="px-5 py-2 bg-error text-on-tertiary font-bold rounded hover:bg-red-700 transition-all cursor-pointer active:scale-95 flex items-center gap-2">
                <span v-if="submitting" class="w-3.5 h-3.5 border-2 border-white border-t-transparent rounded-full animate-spin"></span>
                <span>Hapus</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </Transition>

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
import { ref, computed, onMounted } from 'vue'
import { api } from '../../services/api.js'
import Sidebar from '../../components/Sidebar.vue'

// Sidebar state
const sidebarOpen = ref(false)

// Data state
const riwayatList = ref([])
const loading = ref(false)
const searchQuery = ref('')

// Pagination
const currentPage = ref(1)
const itemsPerPage = ref(8)

// Modals
const detailOpen = ref(false)
const selectedItem = ref(null)

const deleteModalOpen = ref(false)
const itemToDelete = ref(null)
const submitting = ref(false)

// Toast
const toasts = ref([])
let toastIdCounter = 0

// ── Computed: filtered history ─────────────────────────────────
const filteredRiwayat = computed(() => {
  const q = searchQuery.value.trim().toLowerCase()
  if (!q) return riwayatList.value
  return riwayatList.value.filter(r => 
    r.name.toLowerCase().includes(q) || r.diagnosis.toLowerCase().includes(q)
  )
})

// ── Computed: Top diagnosis ────────────────────────────────────
const topDiagnosisName = computed(() => {
  if (riwayatList.value.length === 0) return 'Belum ada data'
  const countMap = {}
  riwayatList.value.forEach(r => {
    countMap[r.diagnosis] = (countMap[r.diagnosis] || 0) + 1
  })
  let max = 0
  let topName = '-'
  for (const [name, count] of Object.entries(countMap)) {
    if (count > max) {
      max = count
      topName = name
    }
  }
  return topName
})

// ── Computed: Pagination ───────────────────────────────────────
const totalPages = computed(() => {
  return Math.ceil(filteredRiwayat.value.length / itemsPerPage.value) || 1
})

const paginatedRiwayat = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value
  const end = start + itemsPerPage.value
  return filteredRiwayat.value.slice(start, end)
})

const pageStartIndex = computed(() => {
  if (filteredRiwayat.value.length === 0) return 0
  return (currentPage.value - 1) * itemsPerPage.value + 1
})

const pageEndIndex = computed(() => {
  return Math.min(currentPage.value * itemsPerPage.value, filteredRiwayat.value.length)
})

// ── Styling Badge ──────────────────────────────────────────────
const getBadgeCls = (prob) => {
  if (prob >= 0.75) return 'bg-[#E6F4EA] text-[#1E8E3E] border-[#1E8E3E]/20'
  if (prob <= 0.45) return 'bg-[#FCE8E6] text-[#D93025] border-[#D93025]/20'
  return 'bg-[#FFF4E5] text-[#B06000] border-[#B06000]/20'
}

const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  try {
    const d = new Date(dateStr)
    return d.toLocaleString('id-ID', { dateStyle: 'short', timeStyle: 'short' })
  } catch {
    return dateStr
  }
}

// ── Toast Helpers ──────────────────────────────────────────────
const showToast = (type, message) => {
  const id = toastIdCounter++
  toasts.value.push({ id, type, message })
  setTimeout(() => removeToast(id), 4500)
}
const removeToast = (id) => { toasts.value = toasts.value.filter(t => t.id !== id) }

// ── API Operations ─────────────────────────────────────────────
const fetchRiwayat = async () => {
  loading.value = true
  try {
    const res = await api.getRiwayat()
    riwayatList.value = res.success ? res.data : []
  } catch (err) {
    showToast('error', 'Gagal memuat riwayat: ' + err.message)
  } finally {
    loading.value = false
  }
}

const viewDetail = (item) => {
  selectedItem.value = item
  detailOpen.value = true
}

const confirmDelete = (item) => {
  itemToDelete.value = item
  deleteModalOpen.value = true
}

const closeDeleteModal = () => {
  if (!submitting.value) {
    deleteModalOpen.value = false
    itemToDelete.value = null
  }
}

const handleDelete = async () => {
  if (!itemToDelete.value) return
  submitting.value = true
  try {
    const res = await api.deleteRiwayat(itemToDelete.value.id)
    if (res.success) {
      showToast('success', 'Record diagnosa berhasil dihapus.')
      deleteModalOpen.value = false
      itemToDelete.value = null
      await fetchRiwayat()
    }
  } catch (err) {
    showToast('error', err.message)
  } finally {
    submitting.value = false
  }
}

onMounted(fetchRiwayat)
</script>

<style scoped>
.modal-fade-enter-active, .modal-fade-leave-active { transition: opacity 0.25s ease; }
.modal-fade-enter-from, .modal-fade-leave-to       { opacity: 0; }
@keyframes modal-pop {
  from { transform: scale(0.95); opacity: 0; }
  to   { transform: scale(1);   opacity: 1; }
}
.animate-modal-pop { animation: modal-pop 0.2s cubic-bezier(0.16, 1, 0.3, 1) forwards; }
.toast-list-enter-active { transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275); }
.toast-list-leave-active { transition: all 0.2s ease-in; position: absolute; }
.toast-list-enter-from   { transform: translateY(20px) scale(0.9); opacity: 0; }
.toast-list-leave-to     { transform: translateX(100px); opacity: 0; }
</style>
