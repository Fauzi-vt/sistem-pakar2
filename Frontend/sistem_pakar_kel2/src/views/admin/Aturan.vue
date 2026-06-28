<template>
  <div class="min-h-screen bg-background text-on-background font-body-md flex relative antialiased">
    <!-- Side Navigation -->
    <Sidebar v-model:isOpen="sidebarOpen" />

    <!-- Main Content Area -->
    <div class="flex-1 flex flex-col min-h-screen lg:ml-64 transition-all duration-300">
      
      <!-- Top Navigation Header -->
      <header class="bg-surface-container-lowest dark:bg-surface-container flex justify-between items-center w-full px-container-padding h-16 sticky top-0 z-40 border-b border-outline-variant">
        <!-- Left: Toggle & Title Info -->
        <div class="flex items-center gap-4 w-full lg:w-1/2">
          <button @click="sidebarOpen = !sidebarOpen" 
                  class="lg:hidden flex items-center justify-center p-2 bg-surface-container rounded-lg text-on-surface hover:bg-surface-container-high transition-colors">
            <span class="material-symbols-outlined">menu</span>
          </button>
          <div>
            <h1 class="font-headline-sm text-headline-sm font-bold text-primary truncate leading-tight">Basis Pengetahuan</h1>
            <p class="text-xs text-on-surface-variant hidden sm:block mt-0.5">Matriks relasi penyakit, gejala, dan bobot pakar (Certainty Factor).</p>
          </div>
        </div>

        <!-- Right: Actions -->
        <div class="flex items-center gap-stack-md shrink-0">
          <button @click="exportToCSV"
            class="bg-surface-container-lowest border border-outline-variant text-on-surface font-label-md py-2.5 px-4 rounded flex items-center justify-center gap-2 hover:bg-surface-container transition-all cursor-pointer active:scale-95">
            <span class="material-symbols-outlined text-[18px]">download</span>
            Ekspor CSV
          </button>
          <button @click="openCreateModal"
            class="bg-primary-container text-on-tertiary font-label-md py-2.5 px-4 rounded flex items-center justify-center gap-2 hover:bg-primary transition-all cursor-pointer active:scale-95">
            <span class="material-symbols-outlined text-[18px]">add</span>
            Tambah Relasi
          </button>
        </div>
      </header>

      <!-- Main Canvas -->
      <main class="p-container-padding flex-1 flex flex-col gap-stack-lg">
        
        <!-- Filter & Search Section -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-gutter items-center p-4 bg-surface-container-lowest border border-outline-variant rounded hover:shadow-[0_4px_12px_rgba(26,54,93,0.02)] transition-shadow">
          <!-- Search input -->
          <div class="md:col-span-2 relative w-full">
            <span class="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-on-surface-variant">search</span>
            <input 
              v-model="searchQuery"
              @input="currentPage = 1"
              class="w-full bg-surface-container-lowest border border-outline-variant rounded pl-10 pr-4 py-2 font-body-sm text-on-surface focus:border-secondary focus:ring-1 focus:ring-secondary outline-none transition-all" 
              placeholder="Cari penyakit atau gejala..." 
              type="text"
            >
          </div>
          <!-- Dropdown Filter -->
          <div class="flex items-center gap-2 w-full">
            <span class="text-xs font-semibold text-on-surface-variant shrink-0">Filter Penyakit:</span>
            <select
              v-model="selectedFilterPenyakitId"
              @change="currentPage = 1"
              class="w-full bg-surface-container-lowest border border-outline-variant rounded px-3 py-2 text-xs font-medium text-on-surface focus:border-secondary focus:ring-1 focus:ring-secondary outline-none transition-all cursor-pointer"
            >
              <option :value="null">Semua Penyakit</option>
              <option v-for="p in penyakitList" :key="p.id" :value="p.id">
                [{{ p.kode }}] {{ p.nama }}
              </option>
            </select>
          </div>
        </div>

        <!-- Main Data Table Container -->
        <section class="bg-surface-container-lowest border border-outline-variant rounded flex flex-col">
          <div class="overflow-x-auto">
            <table class="w-full text-left border-collapse">
              <thead>
                <tr class="border-b border-primary bg-background">
                  <th class="p-4 pl-6 font-label-sm text-label-sm text-on-surface-variant uppercase tracking-wider w-32">ID Relasi</th>
                  <th class="p-4 font-label-sm text-label-sm text-on-surface-variant uppercase tracking-wider w-1/3">Penyakit (Hipotesis)</th>
                  <th class="p-4 font-label-sm text-label-sm text-on-surface-variant uppercase tracking-wider">Gejala (Evidence)</th>
                  <th class="p-4 font-label-sm text-label-sm text-on-surface-variant uppercase tracking-wider w-44">Bobot Pakar (CF)</th>
                  <th class="p-4 pr-6 font-label-sm text-label-sm text-on-surface-variant uppercase tracking-wider text-right w-28">Aksi</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-outline-variant/30">
                <tr v-if="loading">
                  <td colspan="5" class="p-12 text-center text-on-surface-variant">
                    <div class="flex items-center justify-center gap-2">
                      <span class="w-4 h-4 border-2 border-t-transparent rounded-full animate-spin border-primary"></span>
                      <span>Memuat data basis pengetahuan...</span>
                    </div>
                  </td>
                </tr>
                <tr v-else-if="filteredRules.length === 0">
                  <td colspan="5" class="p-12 text-center text-on-surface-variant italic">Tidak ada relasi basis pengetahuan</td>
                </tr>
                
                <tr v-else v-for="(row, idx) in paginatedRules" :key="row.id"
                    class="bg-surface-container-lowest hover:bg-surface-container-low transition-colors">
                  <!-- ID Relasi -->
                  <td class="p-4 pl-6">
                    <span class="font-bold text-primary tracking-wider">{{ row.relasi_code }}</span>
                  </td>
                  
                  <!-- Penyakit -->
                  <td class="p-4">
                    <div class="flex items-center gap-2">
                      <span class="w-2.5 h-2.5 rounded-full shrink-0" :class="row.dotCls"></span>
                      <div class="font-body-md text-primary font-bold">
                        {{ row.penyakit_kode }} - {{ row.penyakit_nama }}
                      </div>
                    </div>
                  </td>
                  
                  <!-- Gejala -->
                  <td class="p-4">
                    <div class="font-body-sm text-on-surface leading-relaxed">
                      {{ row.gejala_kode }} - {{ row.gejala_nama }}
                    </div>
                  </td>

                  <!-- Bobot (CF) -->
                  <td class="p-4">
                    <span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-bold border" :class="row.badgeCls">
                      {{ row.probability.toFixed(2) }}
                    </span>
                  </td>
                  
                  <!-- Aksi -->
                  <td class="p-4 pr-6 text-right">
                    <div class="flex items-center justify-end gap-2">
                      <button @click="openEditModal(row)"
                              class="text-secondary hover:text-primary p-1.5 rounded hover:bg-surface-container-high transition-colors cursor-pointer"
                              title="Edit Relasi">
                        <span class="material-symbols-outlined text-[20px]">edit</span>
                      </button>
                      <button @click="confirmDelete(row)"
                              class="text-error hover:text-on-error-container p-1.5 rounded hover:bg-error-container/30 transition-colors cursor-pointer"
                              title="Hapus Relasi">
                        <span class="material-symbols-outlined text-[20px]">delete</span>
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Pagination Footer matching mockup design -->
          <div v-if="filteredRules.length > 0" 
               class="p-4 border-t border-outline-variant/50 flex flex-col sm:flex-row items-center justify-between gap-4">
            <span class="font-body-sm text-body-sm text-on-surface-variant">
              Menampilkan {{ pageStartIndex }}-{{ pageEndIndex }} dari {{ filteredRules.length }} relasi
            </span>
            <div class="flex items-center gap-1">
              <!-- Prev page -->
              <button @click="currentPage > 1 && currentPage--" 
                      :disabled="currentPage === 1"
                      class="w-8 h-8 rounded border border-outline-variant flex items-center justify-center hover:bg-surface-container-low cursor-pointer disabled:opacity-40 disabled:cursor-not-allowed transition-colors text-on-surface">
                <span class="material-symbols-outlined text-base">chevron_left</span>
              </button>
              
              <!-- Pages -->
              <button v-for="page in totalPages" :key="page"
                      @click="currentPage = page"
                      class="w-8 h-8 rounded text-sm font-semibold flex items-center justify-center transition-colors cursor-pointer"
                      :class="currentPage === page 
                        ? 'bg-primary text-on-tertiary font-bold' 
                        : 'border border-outline-variant text-on-surface hover:bg-surface-container-low'">
                {{ page }}
              </button>

              <!-- Next page -->
              <button @click="currentPage < totalPages && currentPage++" 
                      :disabled="currentPage === totalPages"
                      class="w-8 h-8 rounded border border-outline-variant flex items-center justify-center hover:bg-surface-container-low cursor-pointer disabled:opacity-40 disabled:cursor-not-allowed transition-colors text-on-surface">
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

    <!-- ── FORM MODAL (Add / Edit) ── -->
    <Transition name="modal-fade">
      <div v-if="modalOpen" class="fixed inset-0 z-50 flex items-center justify-center p-4">
        <!-- Overlay -->
        <div @click="closeModal" class="absolute inset-0 bg-inverse-surface/60 backdrop-blur-sm"></div>

        <!-- Dialog Box -->
        <div class="relative w-full max-w-lg bg-surface-container-lowest rounded-xl shadow-2xl overflow-hidden border border-outline-variant animate-modal-pop">
          <!-- Header -->
          <div class="flex items-center justify-between px-6 py-4 border-b border-outline-variant bg-surface-container-low">
            <h3 class="font-bold text-primary flex items-center gap-2">
              <span class="w-2.5 h-2.5 rounded-full bg-secondary"></span>
              {{ isEditing ? 'Edit Relasi Aturan' : 'Tambah Relasi Baru' }}
            </h3>
            <button @click="closeModal" class="text-on-surface-variant hover:text-on-surface cursor-pointer">
              <span class="material-symbols-outlined text-lg">close</span>
            </button>
          </div>

          <!-- Body Form -->
          <form @submit.prevent="handleSubmit" class="p-6 space-y-4 text-sm">
            <div v-if="formError" class="p-3 bg-error-container text-on-error-container rounded-lg border border-error/20 flex gap-2 items-start text-xs">
              <span class="material-symbols-outlined text-base">warning</span>
              <span>{{ formError }}</span>
            </div>

            <!-- Penyakit Dropdown -->
            <div>
              <label class="block font-bold text-xs uppercase tracking-wider mb-1.5 text-on-surface-variant">Penyakit (Hipotesis) <span class="text-error">*</span></label>
              <select
                v-model="formData.penyakit_id"
                required
                :disabled="isEditing"
                class="w-full bg-surface-container-lowest border border-outline-variant rounded px-4 py-2 text-on-surface focus:border-secondary focus:ring-1 focus:ring-secondary outline-none transition-all cursor-pointer disabled:opacity-50"
              >
                <option :value="''" disabled>-- Pilih Penyakit --</option>
                <option v-for="p in penyakitList" :key="p.id" :value="p.id">
                  [{{ p.kode }}] {{ p.nama }}
                </option>
              </select>
            </div>

            <!-- Gejala Dropdown -->
            <div>
              <label class="block font-bold text-xs uppercase tracking-wider mb-1.5 text-on-surface-variant">Gejala (Evidence) <span class="text-error">*</span></label>
              <select
                v-model="formData.gejala_id"
                required
                :disabled="isEditing"
                class="w-full bg-surface-container-lowest border border-outline-variant rounded px-4 py-2 text-on-surface focus:border-secondary focus:ring-1 focus:ring-secondary outline-none transition-all cursor-pointer disabled:opacity-50"
              >
                <option :value="''" disabled>-- Pilih Gejala --</option>
                <option v-for="g in gejalaList" :key="g.id" :value="g.id">
                  [{{ g.kode }}] {{ g.nama }}
                </option>
              </select>
            </div>

            <!-- Conditional Probability Value / Weight -->
            <div>
              <label class="block font-bold text-xs uppercase tracking-wider mb-1.5 text-on-surface-variant">Bobot Pakar / Probabilitas Kondisional <span class="text-error">*</span></label>
              <input
                v-model="formData.conditional_probability"
                type="number"
                step="0.01"
                min="0"
                max="1"
                required
                placeholder="Contoh: 0.85"
                class="w-full bg-surface-container-lowest border border-outline-variant rounded px-4 py-2 text-on-surface focus:border-secondary focus:ring-1 focus:ring-secondary outline-none transition-all"
              />
              <p class="text-[10px] mt-1 text-on-surface-variant">Masukkan bobot nilai antara 0.00 sampai 1.00</p>
            </div>

            <!-- Action buttons -->
            <div class="flex items-center justify-end gap-3 pt-4 border-t border-outline-variant/50">
              <button
                type="button"
                @click="closeModal"
                class="px-4 py-2 border border-outline-variant rounded font-semibold hover:bg-surface-container-low transition-colors cursor-pointer text-on-surface"
              >
                Batal
              </button>
              <button
                type="submit"
                :disabled="submitting"
                class="px-5 py-2 bg-primary text-on-tertiary font-bold rounded hover:bg-primary-container transition-all cursor-pointer active:scale-95 flex items-center gap-2"
              >
                <span v-if="submitting" class="w-3.5 h-3.5 border-2 border-white border-t-transparent rounded-full animate-spin"></span>
                <span>{{ isEditing ? 'Simpan Perubahan' : 'Tambah Relasi' }}</span>
              </button>
            </div>
          </form>
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

            <h3 class="font-bold text-lg mb-2 text-primary">Hapus Relasi?</h3>
            <p class="text-sm mb-6 leading-relaxed text-on-surface-variant">
              Apakah Anda yakin ingin menghapus relasi <strong class="text-primary">{{ ruleToDelete?.relasi_code }}</strong> 
              yang menghubungkan <strong class="text-primary">{{ ruleToDelete?.penyakit_nama }}</strong> 
              dan <strong class="text-primary">{{ ruleToDelete?.gejala_nama }}</strong>?
              <br><span class="text-xs mt-1 block text-error font-semibold">Tindakan ini permanen dan tidak dapat dibatalkan.</span>
            </p>

            <div class="flex items-center justify-center gap-3">
              <button
                type="button"
                @click="closeDeleteModal"
                class="px-4 py-2 border border-outline-variant rounded font-semibold hover:bg-surface-container-low transition-colors cursor-pointer text-on-surface"
              >
                Batal
              </button>
              <button
                type="button"
                @click="handleDelete"
                :disabled="submitting"
                class="px-5 py-2 bg-error text-on-tertiary font-bold rounded hover:bg-red-700 transition-all cursor-pointer active:scale-95 flex items-center gap-2"
              >
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
        <div
          v-for="toast in toasts"
          :key="toast.id"
          class="flex items-start gap-3 p-4 bg-surface-container-lowest rounded-xl border shadow-2xl transition-all duration-300 border-outline-variant/60"
        >
          <div class="mt-0.5 shrink-0">
            <span v-if="toast.type === 'success'" class="material-symbols-outlined text-secondary">check_circle</span>
            <span v-else class="material-symbols-outlined text-error">error</span>
          </div>

          <div class="flex-1">
            <p class="text-sm font-bold leading-tight text-primary">
              {{ toast.type === 'success' ? 'Sukses' : 'Gagal' }}
            </p>
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

const sidebarOpen = ref(false)

// ── State variables ───────────────────────────────────────────
const penyakitList = ref([])
const gejalaList = ref([])
const rulesList = ref([])
const loading = ref(false)
const searchQuery = ref('')
const selectedFilterPenyakitId = ref(null)

// Pagination State
const currentPage = ref(1)
const itemsPerPage = ref(5)

// Modal State
const modalOpen = ref(false)
const isEditing = ref(false)
const submitting = ref(false)
const formError = ref(null)
const formData = ref({
  id: '',
  penyakit_id: '',
  gejala_id: '',
  conditional_probability: 0.0
})

// Delete Modal State
const deleteModalOpen = ref(false)
const ruleToDelete = ref(null)

// Toast State
const toasts = ref([])
let toastIdCounter = 0

// ── Color dot picking based on disease code ────────────────────
const getDotCls = (kode) => {
  const codeInt = parseInt(kode.replace(/\D/g, '')) || 0
  const colors = [
    'bg-red-500',
    'bg-blue-500',
    'bg-emerald-500',
    'bg-amber-500',
    'bg-purple-500',
    'bg-pink-500',
    'bg-indigo-500'
  ]
  return colors[codeInt % colors.length]
}

// ── Badge color based on CF weight ─────────────────────────────
const getBadgeCls = (prob) => {
  if (prob >= 0.75) {
    return 'bg-[#E6F4EA] text-[#1E8E3E] border-[#1E8E3E]/20'
  } else if (prob <= 0.45) {
    return 'bg-[#FCE8E6] text-[#D93025] border-[#D93025]/20'
  }
  return 'bg-[#FFF4E5] text-[#B06000] border-[#B06000]/20'
}

// ── Computed Filtered Rules ────────────────────────────────────
const filteredRules = computed(() => {
  let list = rulesList.value

  // Filter by selected disease
  if (selectedFilterPenyakitId.value !== null) {
    list = list.filter(r => r.penyakit_id === selectedFilterPenyakitId.value)
  }

  // Filter by query search
  const q = searchQuery.value.trim().toLowerCase()
  if (q) {
    list = list.filter(r => 
      r.penyakit_kode.toLowerCase().includes(q) ||
      r.penyakit_nama.toLowerCase().includes(q) ||
      r.gejala_kode.toLowerCase().includes(q) ||
      r.gejala_nama.toLowerCase().includes(q)
    )
  }

  // Add Padded IDs and styling tags
  return list.map((item, idx) => ({
    ...item,
    relasi_code: `R-${String(idx + 1).padStart(3, '0')}`,
    dotCls: getDotCls(item.penyakit_kode),
    badgeCls: getBadgeCls(item.probability)
  }))
})

// ── Computed: pagination logic ────────────────────────────────
const totalPages = computed(() => {
  return Math.ceil(filteredRules.value.length / itemsPerPage.value) || 1
})

const paginatedRules = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value
  const end = start + itemsPerPage.value
  return filteredRules.value.slice(start, end)
})

const pageStartIndex = computed(() => {
  if (filteredRules.value.length === 0) return 0
  return (currentPage.value - 1) * itemsPerPage.value + 1
})

const pageEndIndex = computed(() => {
  return Math.min(currentPage.value * itemsPerPage.value, filteredRules.value.length)
})

// ── API Fetching ──────────────────────────────────────────────
const fetchPenyakit = async () => {
  try {
    const res = await fetch('http://127.0.0.1:8000/api/penyakit-full').then(r => r.json())
    if (res.success) {
      penyakitList.value = res.data
    }
  } catch (err) {
    console.error('Fetch penyakit error:', err)
  }
}

const fetchGejala = async () => {
  try {
    const res = await api.getGejala()
    if (res.success) {
      gejalaList.value = res.data
    }
  } catch (err) {
    console.error('Fetch gejala error:', err)
  }
}

const fetchRules = async () => {
  loading.value = true
  try {
    const res = await api.getAturan()
    if (res.success && Array.isArray(res.data)) {
      rulesList.value = res.data.map(r => ({
        id: r.id,
        penyakit_id: r.penyakit_id,
        penyakit_kode: r.penyakit?.kode_penyakit || '?',
        penyakit_nama: r.penyakit?.nama_penyakit || '?',
        gejala_id: r.gejala_id,
        gejala_kode: r.gejala?.kode_gejala || '?',
        gejala_nama: r.gejala?.nama_gejala || '?',
        probability: r.conditional_probability ?? 0.0
      }))
    }
  } catch (err) {
    showToast('error', 'Gagal memuat rules: ' + err.message)
  } finally {
    loading.value = false
  }
}

// ── Toast Functions ───────────────────────────────────────────
const showToast = (type, message) => {
  const id = toastIdCounter++
  toasts.value.push({ id, type, message })
  setTimeout(() => removeToast(id), 4500)
}
const removeToast = (id) => { toasts.value = toasts.value.filter(t => t.id !== id) }

// ── Export CSV ────────────────────────────────────────────────
const exportToCSV = () => {
  if (filteredRules.value.length === 0) {
    showToast('error', 'Tidak ada data relasi untuk diekspor.')
    return
  }
  const headers = ['ID Relasi', 'Penyakit (Hipotesis)', 'Gejala (Evidence)', 'Bobot Pakar (CF)']
  const rows = filteredRules.value.map(row => [
    row.relasi_code,
    `[${row.penyakit_kode}] ${row.penyakit_nama}`,
    `[${row.gejala_kode}] ${row.gejala_nama}`,
    row.probability.toFixed(2)
  ])
  
  const csvContent = "\uFEFF" + [headers.join(','), ...rows.map(e => e.map(val => `"${val}"`).join(","))].join("\n")
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
  const url = URL.createObjectURL(blob)
  const link = document.createElement("a")
  link.setAttribute("href", url)
  link.setAttribute("download", "basis-pengetahuan.csv")
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  showToast('success', 'Relasi basis pengetahuan berhasil diekspor ke CSV.')
}

// ── Modal Actions ──────────────────────────────────────────────
const openCreateModal = () => {
  isEditing.value = false
  formError.value = null
  formData.value = {
    id: '',
    penyakit_id: '',
    gejala_id: '',
    conditional_probability: 0.0
  }
  modalOpen.value = true
}

const openEditModal = (row) => {
  isEditing.value = true
  formError.value = null
  formData.value = {
    id: row.id,
    penyakit_id: row.penyakit_id,
    gejala_id: row.gejala_id,
    conditional_probability: row.probability
  }
  modalOpen.value = true
}

const closeModal = () => { if (!submitting.value) modalOpen.value = false }

// ── Handle Submit (Add / Edit) ─────────────────────────────────
const handleSubmit = async () => {
  if (!formData.value.penyakit_id || !formData.value.gejala_id) {
    formError.value = 'Penyakit dan Gejala wajib dipilih.'
    return
  }
  const val = parseFloat(formData.value.conditional_probability)
  if (isNaN(val) || val < 0 || val > 1) {
    formError.value = 'Bobot pakar / probabilitas kondisional harus antara 0.00 sampai 1.00.'
    return
  }

  submitting.value = true
  formError.value = null

  try {
    const payload = {
      penyakit_id: parseInt(formData.value.penyakit_id),
      gejala_id: parseInt(formData.value.gejala_id),
      conditional_probability: val
    }

    if (isEditing.value) {
      const res = await api.updateAturan(formData.value.id, payload)
      if (res.success) {
        showToast('success', 'Relasi basis pengetahuan berhasil diperbarui.')
        modalOpen.value = false
        await fetchRules()
      }
    } else {
      const res = await api.createAturan(payload)
      if (res.success) {
        showToast('success', 'Relasi basis pengetahuan berhasil ditambahkan.')
        modalOpen.value = false
        await fetchRules()
      }
    }
  } catch (err) {
    formError.value = err.message || 'Terjadi kesalahan saat memproses data.'
    showToast('error', formError.value)
  } finally {
    submitting.value = false
  }
}

// ── Handle Delete ──────────────────────────────────────────────
const confirmDelete = (row) => {
  ruleToDelete.value = row
  deleteModalOpen.value = true
}

const closeDeleteModal = () => { if (!submitting.value) deleteModalOpen.value = false }

const handleDelete = async () => {
  if (!ruleToDelete.value) return
  submitting.value = true
  try {
    const res = await api.deleteAturan(ruleToDelete.value.id)
    if (res.success) {
      showToast('success', 'Relasi basis pengetahuan berhasil dihapus.')
      deleteModalOpen.value = false
      ruleToDelete.value = null
      await fetchRules()
    }
  } catch (err) {
    showToast('error', err.message || 'Terjadi kesalahan saat menghapus data.')
  } finally {
    submitting.value = false
  }
}

onMounted(() => {
  fetchPenyakit()
  fetchGejala()
  fetchRules()
})
</script>

<style scoped>
.modal-fade-enter-active, .modal-fade-leave-active { transition: opacity 0.25s ease-out; }
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
.slide-down-enter-active { transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1); }
.slide-down-leave-active { transition: all 0.2s ease-in; }
.slide-down-enter-from   { opacity: 0; transform: translateY(-8px); }
.slide-down-leave-to     { opacity: 0; transform: translateY(-4px); }
</style>
