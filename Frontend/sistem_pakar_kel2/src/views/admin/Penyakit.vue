<template>
  <div class="min-h-screen bg-background text-on-background font-body-md flex relative antialiased">
    <!-- Side Navigation -->
    <Sidebar v-model:isOpen="sidebarOpen" />

    <!-- Main Content Area -->
    <div class="flex-1 flex flex-col min-h-screen lg:ml-64 transition-all duration-300">
      
      <!-- Top Navigation Header -->
      <header class="bg-surface-container-lowest dark:bg-surface-container flex justify-between items-center w-full px-container-padding h-16 sticky top-0 z-40 border-b border-outline-variant">
        <!-- Left: Search and Toggle (Only shown when table is visible) -->
        <div class="flex items-center gap-4 w-full lg:w-1/3">
          <button @click="sidebarOpen = !sidebarOpen" 
                  class="lg:hidden flex items-center justify-center p-2 bg-surface-container rounded-lg text-on-surface hover:bg-surface-container-high transition-colors">
            <span class="material-symbols-outlined">menu</span>
          </button>
          <div v-if="!showFormView" class="relative w-full hidden sm:block">
            <span class="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-on-surface-variant">search</span>
            <input 
              v-model="searchQuery"
              @input="currentPage = 1"
              class="w-full bg-surface-container-lowest border border-outline-variant rounded pl-10 pr-4 py-2 font-body-sm text-on-surface focus:border-secondary focus:ring-1 focus:ring-secondary outline-none transition-all" 
              placeholder="Cari penyakit..." 
              type="text"
            >
          </div>
        </div>

        <!-- Right: Actions -->
        <div class="flex items-center gap-stack-md shrink-0">
          <button v-if="!showFormView" @click="openCreateModal"
            class="bg-primary-container text-on-tertiary font-label-md py-2.5 px-4 rounded flex items-center justify-center gap-2 hover:bg-primary transition-all cursor-pointer active:scale-95">
            <span class="material-symbols-outlined text-[18px]">add</span>
            Tambah Penyakit Baru
          </button>
        </div>
      </header>

      <!-- Main Canvas -->
      <main class="p-container-padding flex-1 flex flex-col gap-stack-lg">
        
        <!-- Table List View -->
        <div v-if="!showFormView" class="flex flex-col gap-stack-lg">
          <!-- Page Title -->
          <div>
            <h2 class="font-headline-md text-headline-md text-primary">Manajemen Data Penyakit</h2>
          </div>

          <!-- Metrics cards matching mockup layout -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-gutter">
            
            <!-- Card 1: Total Penyakit -->
            <div class="bg-surface-container-lowest border border-outline-variant rounded p-stack-md flex flex-col gap-stack-sm hover:shadow-[0_4px_12px_rgba(26,54,93,0.05)] transition-shadow">
              <div class="flex justify-between items-center text-on-surface-variant">
                <span class="font-label-sm text-label-sm uppercase tracking-wider">Total Penyakit</span>
                <span class="material-symbols-outlined text-[20px]">settings</span>
              </div>
              <div class="font-headline-lg text-headline-lg text-primary">{{ diseases.length }}</div>
            </div>

            <!-- Card 2: Status Basis Pengetahuan -->
            <div class="md:col-span-2 bg-surface-container-lowest border border-outline-variant rounded p-stack-md flex flex-col gap-unit hover:shadow-[0_4px_12px_rgba(26,54,93,0.05)] transition-shadow">
              <div class="flex justify-between items-center text-on-surface-variant">
                <span class="font-label-sm text-label-sm uppercase tracking-wider">Status Basis Pengetahuan</span>
                <span class="material-symbols-outlined text-[20px] text-secondary">check_circle</span>
              </div>
              <div class="font-body-md font-bold text-primary mt-1">Sistem pakar THT saat ini aktif.</div>
              <div class="font-body-sm text-body-sm text-on-surface-variant">
                Pastikan relasi penyakit dan gejala mutakhir.
              </div>
            </div>

          </div>

          <!-- Main Data Table Container -->
          <section class="bg-surface-container-lowest border border-outline-variant rounded flex flex-col">
            <div class="overflow-x-auto">
              <table class="w-full text-left border-collapse">
                <thead>
                  <tr class="border-b border-primary bg-background">
                    <th class="p-4 pl-6 font-label-sm text-label-sm text-on-surface-variant uppercase tracking-wider w-28">Kode</th>
                    <th class="p-4 font-label-sm text-label-sm text-on-surface-variant uppercase tracking-wider w-1/4">Nama Penyakit</th>
                    <th class="p-4 font-label-sm text-label-sm text-on-surface-variant uppercase tracking-wider">Deskripsi Singkat</th>
                    <th class="p-4 pr-6 font-label-sm text-label-sm text-on-surface-variant uppercase tracking-wider text-right w-36">Aksi</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-outline-variant/30">
                  <tr v-if="loading">
                    <td colspan="4" class="p-12 text-center text-on-surface-variant">
                      <div class="flex items-center justify-center gap-2">
                        <span class="w-4 h-4 border-2 border-t-transparent rounded-full animate-spin border-primary"></span>
                        <span>Memuat data penyakit...</span>
                      </div>
                    </td>
                  </tr>
                  <tr v-else-if="filteredDiseases.length === 0">
                    <td colspan="4" class="p-12 text-center text-on-surface-variant italic">Tidak ada data penyakit</td>
                  </tr>
                  
                  <tr v-else v-for="disease in paginatedDiseases" :key="disease.id"
                      class="bg-surface-container-lowest hover:bg-surface-container-low transition-colors">
                    <!-- Kode -->
                    <td class="p-4 pl-6">
                      <span class="font-bold text-primary tracking-wider">{{ disease.kode }}</span>
                    </td>
                    
                    <!-- Nama -->
                    <td class="p-4">
                      <div class="font-body-md text-primary font-bold">{{ disease.nama }}</div>
                    </td>
                    
                    <!-- Deskripsi -->
                    <td class="p-4">
                      <div class="font-body-sm text-on-surface-variant leading-relaxed line-clamp-2">
                        {{ disease.deskripsi || '-' }}
                      </div>
                    </td>
                    
                    <!-- Aksi -->
                    <td class="p-4 pr-6 text-right">
                      <div class="flex items-center justify-end gap-2.5">
                        <button @click="openEditModal(disease)"
                                class="text-secondary hover:text-primary p-1.5 rounded hover:bg-surface-container-high transition-colors cursor-pointer"
                                title="Edit Penyakit">
                          <span class="material-symbols-outlined text-[20px]">edit</span>
                        </button>
                        <button @click="confirmDelete(disease)"
                                class="text-error hover:text-on-error-container p-1.5 rounded hover:bg-error-container/30 transition-colors cursor-pointer"
                                title="Hapus Penyakit">
                          <span class="material-symbols-outlined text-[20px]">delete</span>
                        </button>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            <!-- Pagination Footer -->
            <div v-if="filteredDiseases.length > 0" 
                 class="p-4 border-t border-outline-variant/50 flex flex-col sm:flex-row items-center justify-between gap-4">
              <span class="font-body-sm text-body-sm text-on-surface-variant">
                Menampilkan {{ pageStartIndex }}-{{ pageEndIndex }} dari {{ filteredDiseases.length }} penyakit
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
        </div>

        <!-- Dedicated Bento Form View -->
        <div v-else class="flex flex-col gap-stack-lg animate-modal-pop">
          <!-- Breadcrumbs / Page Title -->
          <div>
            <div class="flex items-center gap-2 text-on-surface-variant font-label-sm text-label-sm mb-2">
              <button @click="showFormView = false" class="hover:text-primary transition-colors cursor-pointer">Data Penyakit</button>
              <span class="material-symbols-outlined text-[16px]">chevron_right</span>
              <span class="text-primary font-semibold">{{ isEditing ? 'Edit Detail Penyakit' : 'Tambah Penyakit Baru' }}</span>
            </div>
            <h1 class="font-headline-lg text-headline-lg text-primary">
              {{ isEditing ? 'Edit Detail Penyakit' : 'Tambah Penyakit Baru' }}
            </h1>
            <p class="font-body-sm text-body-sm text-on-surface-variant mt-1 max-w-2xl">
              Masukkan detail klinis untuk penyakit THT baru. Informasi ini akan digunakan dalam mesin inferensi Bayes.
            </p>
          </div>

          <!-- Main Form Card -->
          <div class="bg-surface-container-lowest rounded border border-outline-variant shadow-[0_4px_12px_rgba(26,54,93,0.05)] overflow-hidden w-full max-w-4xl">
            <!-- Card Header -->
            <div class="px-6 py-4 border-b border-outline-variant bg-surface flex justify-between items-center">
              <div class="flex items-center gap-3">
                <div class="w-10 h-10 rounded-full bg-surface-container-low flex items-center justify-center text-primary">
                  <span class="material-symbols-outlined" style="font-variation-settings: 'FILL' 1;">
                    {{ isEditing ? 'edit_document' : 'add_circle' }}
                  </span>
                </div>
                <h2 class="font-headline-sm text-headline-sm text-primary">Informasi Penyakit Utama</h2>
              </div>
              <span class="bg-surface-container-low text-primary font-label-sm text-label-sm px-3 py-1 rounded-full uppercase tracking-wider border border-surface-tint">
                {{ isEditing ? 'Aktif' : 'Draft' }}
              </span>
            </div>

            <!-- Form Fields Container -->
            <form @submit.prevent="handleSubmit">
              <div class="p-6 grid grid-cols-1 md:grid-cols-12 gap-gutter">
                
                <!-- Left Column: Primary Identifiers -->
                <div class="md:col-span-5 flex flex-col gap-4">
                  <!-- Error alert inside form -->
                  <div v-if="formError" class="p-3 bg-error-container text-on-error-container rounded-lg border border-error/20 flex gap-2 items-start text-xs">
                    <span class="material-symbols-outlined text-base">warning</span>
                    <span>{{ formError }}</span>
                  </div>

                  <!-- Kode Penyakit -->
                  <div class="flex flex-col gap-unit">
                    <label class="font-label-md text-label-md text-on-surface" for="kodePenyakit">Kode Penyakit <span class="text-error">*</span></label>
                    <div class="relative">
                      <span class="absolute inset-y-0 left-0 flex items-center pl-3 text-outline">
                        <span class="material-symbols-outlined text-[20px]">tag</span>
                      </span>
                      <input 
                        v-model="formData.kode"
                        :disabled="isEditing"
                        class="w-full pl-10 pr-4 py-2 bg-surface-container-lowest border border-outline-variant rounded font-body-sm text-body-sm text-on-surface focus:outline-none focus:ring-1 focus:ring-secondary focus:border-secondary transition-all placeholder:text-outline-variant disabled:opacity-50" 
                        id="kodePenyakit" 
                        placeholder="e.g., P01" 
                        required 
                        type="text"
                        @input="formData.kode = formData.kode.toUpperCase()"
                      />
                    </div>
                    <p class="font-label-sm text-label-sm text-on-surface-variant mt-1">Kode unik untuk identifikasi basis aturan (e.g., P01, P02).</p>
                  </div>

                  <!-- Nama Penyakit -->
                  <div class="flex flex-col gap-unit mt-2">
                    <label class="font-label-md text-label-md text-on-surface" for="namaPenyakit">Nama Penyakit <span class="text-error">*</span></label>
                    <input 
                      v-model="formData.nama"
                      class="w-full px-4 py-2 bg-surface-container-lowest border border-outline-variant rounded font-body-sm text-body-sm text-on-surface focus:outline-none focus:ring-1 focus:ring-secondary focus:border-secondary transition-all placeholder:text-outline-variant" 
                      id="namaPenyakit" 
                      placeholder="Nama diagnosis klinis..." 
                      required 
                      type="text"
                    />
                  </div>
                </div>

                <!-- Right Column: Detailed Descriptions -->
                <div class="md:col-span-7 flex flex-col gap-4">
                  <!-- Deskripsi Singkat -->
                  <div class="flex flex-col gap-unit">
                    <label class="font-label-md text-label-md text-on-surface" for="deskripsiSingkat">Deskripsi Singkat</label>
                    <textarea 
                      v-model="formData.deskripsi"
                      class="w-full px-4 py-3 bg-surface-container-lowest border border-outline-variant rounded font-body-sm text-body-sm text-on-surface focus:outline-none focus:ring-1 focus:ring-secondary focus:border-secondary transition-all resize-none placeholder:text-outline-variant" 
                      id="deskripsiSingkat" 
                      placeholder="Jelaskan karakteristik umum penyakit..." 
                      rows="3"
                    ></textarea>
                  </div>

                  <!-- Saran Medis / Solusi -->
                  <div class="flex flex-col gap-unit mt-2">
                    <label class="font-label-md text-label-md text-on-surface flex items-center justify-between" for="saranMedis">
                      <span>Saran Medis / Solusi Tindakan <span class="text-error">*</span></span>
                      <span class="material-symbols-outlined text-[18px] text-secondary cursor-help" title="Anjuran yang akan diberikan kepada pasien jika terdiagnosis">info</span>
                    </label>
                    <textarea 
                      v-model="formData.solusi"
                      class="w-full px-4 py-3 bg-surface-container-lowest border border-outline-variant rounded font-body-sm text-body-sm text-on-surface focus:outline-none focus:ring-1 focus:ring-secondary focus:border-secondary transition-all resize-none placeholder:text-outline-variant" 
                      id="saranMedis" 
                      placeholder="Tuliskan rekomendasi pengobatan, anjuran istirahat, atau rujukan spesialis..." 
                      required 
                      rows="4"
                    ></textarea>

                    <!-- Contextual AI Suggestion Chip -->
                    <div class="flex items-center gap-2 mt-2 bg-surface-container-low p-2 rounded border border-outline-variant">
                      <span class="material-symbols-outlined text-secondary text-[18px]">auto_awesome</span>
                      <span class="font-label-sm text-label-sm text-secondary">Gunakan asisten AI untuk menyusun rekomendasi klinis standar.</span>
                      <button @click="generateAISuggestion" class="ml-auto text-secondary font-label-md text-label-md hover:underline cursor-pointer" type="button">Generate</button>
                    </div>
                  </div>
                </div>

              </div>

              <!-- Form Footer Actions -->
              <div class="px-6 py-4 bg-surface border-t border-outline-variant flex justify-end gap-4 items-center">
                <button @click="showFormView = false" class="px-4 py-2 rounded border border-outline text-on-surface-variant font-label-md text-label-md hover:bg-surface-container-low transition-colors outline-none cursor-pointer" type="button">
                  Batal
                </button>
                <button :disabled="submitting" class="px-4 py-2 rounded bg-primary-container text-on-tertiary font-label-md text-label-md hover:bg-primary transition-all outline-none flex items-center gap-2 cursor-pointer disabled:opacity-50" type="submit">
                  <span v-if="submitting" class="w-3.5 h-3.5 border-2 border-white border-t-transparent rounded-full animate-spin"></span>
                  <span v-else class="material-symbols-outlined text-[18px]">save</span>
                  Simpan Penyakit
                </button>
              </div>
            </form>
          </div>
        </div>

      </main>

      <!-- Footer -->
      <footer class="border-t border-outline-variant px-6 py-4 bg-surface-container-lowest shrink-0">
        <p class="text-on-surface-variant text-xs text-center">© 2026 Sistem Pakar THT — Kelompok 2 · RS Jasa Kartini. All rights reserved.</p>
      </footer>
    </div>

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

            <h3 class="font-bold text-lg mb-2 text-primary">Hapus Penyakit?</h3>
            <p class="text-sm mb-6 leading-relaxed text-on-surface-variant">
              Apakah Anda yakin ingin menghapus penyakit <strong class="text-primary">{{ diseaseToDelete?.kode }} - {{ diseaseToDelete?.nama }}</strong>? 
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

// ── State variables ───────────────────────────────────────────
const sidebarOpen = ref(false)
const diseases = ref([])
const searchQuery = ref('')
const loading = ref(false)
const error = ref(null)

// Pagination State
const currentPage = ref(1)
const itemsPerPage = ref(5) // Paginate 5 items per page

// View State for Dedicated Bento Form
const showFormView = ref(false)

// Form Modal State
const isEditing = ref(false)
const submitting = ref(false)
const formError = ref(null)
const formData = ref({
  id: '',
  kode: '',
  nama: '',
  deskripsi: '',
  solusi: ''
})

// Delete Modal State
const deleteModalOpen = ref(false)
const diseaseToDelete = ref(null)

// Toast System State
const toasts = ref([])
let toastIdCounter = 0

// ── Computed: filtered disease list ──────────────────────────
const filteredDiseases = computed(() => {
  const query = searchQuery.value.trim().toLowerCase()
  if (!query) return diseases.value

  return diseases.value.filter(disease => {
    return (
      disease.kode.toLowerCase().includes(query) ||
      disease.nama.toLowerCase().includes(query) ||
      (disease.deskripsi && disease.deskripsi.toLowerCase().includes(query))
    )
  })
})

// ── Computed: pagination logic ────────────────────────────────
const totalPages = computed(() => {
  return Math.ceil(filteredDiseases.value.length / itemsPerPage.value) || 1
})

const paginatedDiseases = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value
  const end = start + itemsPerPage.value
  return filteredDiseases.value.slice(start, end)
})

const pageStartIndex = computed(() => {
  if (filteredDiseases.value.length === 0) return 0
  return (currentPage.value - 1) * itemsPerPage.value + 1
})

const pageEndIndex = computed(() => {
  return Math.min(currentPage.value * itemsPerPage.value, filteredDiseases.value.length)
})

// ── Fetch Diseases ────────────────────────────────────────────
const fetchDiseases = async () => {
  loading.value = true
  error.value = null
  try {
    const response = await api.getPenyakit()
    if (response.success && Array.isArray(response.data)) {
      diseases.value = response.data
    } else {
      diseases.value = []
    }
  } catch (err) {
    console.error('Fetch diseases error:', err)
    error.value = err.message || 'Gagal terhubung ke server.'
    showToast('error', error.value)
  } finally {
    loading.value = false
  }
}

// ── Toast Functions ───────────────────────────────────────────
const showToast = (type, message) => {
  const id = toastIdCounter++
  toasts.value.push({ id, type, message })
  setTimeout(() => {
    removeToast(id)
  }, 4500)
}

const removeToast = (id) => {
  toasts.value = toasts.value.filter(t => t.id !== id)
}

// ── Create Modal Actions (Toggle Form View) ───────────────────
const openCreateModal = () => {
  isEditing.value = false
  formError.value = null
  formData.value = {
    id: '',
    kode: '',
    nama: '',
    deskripsi: '',
    solusi: ''
  }
  showFormView.value = true
}

// ── Edit Modal Actions (Toggle Form View) ─────────────────────
const openEditModal = (disease) => {
  isEditing.value = true
  formError.value = null
  formData.value = {
    id: disease.id,
    kode: disease.kode,
    nama: disease.nama,
    deskripsi: disease.deskripsi || '',
    solusi: disease.solusi || ''
  }
  showFormView.value = true
}

// ── Contextual AI Suggestion Generator ────────────────────────
const generateAISuggestion = () => {
  const name = formData.value.nama.trim().toLowerCase()
  if (!name) {
    showToast('error', 'Silakan ketik nama penyakit terlebih dahulu sebelum generate saran.')
    return
  }

  let suggestion = ''
  if (name.includes('otitis')) {
    suggestion = 'Jaga telinga tetap kering, hindari berenang sementara waktu, jangan bersihkan telinga menggunakan cutton bud, dan gunakan obat tetes telinga yang mengandung antibiotik/kortikosteroid sesuai resep.'
  } else if (name.includes('sinusitis')) {
    suggestion = 'Lakukan inhalasi uap air hangat, gunakan nasal spray dekongestan/saline secara berkala, hindari suhu terlalu dingin/berdebu, dan segera hubungi spesialis THT jika gejala menetap lebih dari 10 hari.'
  } else if (name.includes('faringitis') || name.includes('tenggorokan')) {
    suggestion = 'Istirahat cukup, berkumur dengan air garam hangat minimal 3 kali sehari, perbanyak konsumsi cairan hangat, hindari makanan pedas/gorengan, dan minum antibiotik jika diresepkan oleh dokter.'
  } else if (name.includes('rhinitis') || name.includes('alergi')) {
    suggestion = 'Identifikasi dan hindari agen pemicu alergi (debu, bulu hewan, serbuk sari), gunakan antihistamin oral atau semprot hidung kortikosteroid, serta jaga kelembapan udara ruangan.'
  } else if (name.includes('tonsilitis') || name.includes('amandel')) {
    suggestion = 'Istirahat yang cukup, perbanyak minum air hangat, konsumsi makanan bertekstur lunak, kumur antiseptik hangat, dan konsumsi analgesik/antibiotik sesuai anjuran dokter.'
  } else {
    suggestion = 'Konsultasikan dengan dokter spesialis THT untuk pemeriksaan otoskopi/rinoskopi lebih lanjut. Istirahat cukup, konsumsi air putih minimal 2 liter per hari, dan hindari paparan iritan jalan napas.'
  }

  formData.value.solusi = suggestion
  showToast('success', 'Rekomendasi klinis standar berhasil digenerate oleh asisten.')
}

// ── Submit Handle (Create / Update) ───────────────────────────
const handleSubmit = async () => {
  if (!formData.value.kode.trim() || !formData.value.nama.trim() || !formData.value.solusi.trim()) {
    formError.value = 'Kode, Nama, dan Saran Medis wajib diisi.'
    return
  }

  submitting.value = true
  formError.value = null

  try {
    const payload = {
      kode: formData.value.kode.trim().toUpperCase(),
      nama: formData.value.nama.trim(),
      deskripsi: formData.value.deskripsi.trim(),
      solusi: formData.value.solusi.trim()
    }

    if (isEditing.value) {
      const response = await api.updatePenyakit(formData.value.id, payload)
      if (response.success) {
        showToast('success', `Penyakit '${payload.kode}' berhasil diperbarui.`)
        showFormView.value = false
        await fetchDiseases()
      } else {
        throw new Error(response.message || 'Gagal memperbarui penyakit.')
      }
    } else {
      const response = await api.createPenyakit(payload)
      if (response.success) {
        showToast('success', `Penyakit '${payload.kode}' berhasil ditambahkan.`)
        showFormView.value = false
        await fetchDiseases()
      } else {
        throw new Error(response.message || 'Gagal menambahkan penyakit.')
      }
    }
  } catch (err) {
    console.error('Submit disease error:', err)
    formError.value = err.message || 'Terjadi kesalahan saat memproses data.'
    showToast('error', formError.value)
  } finally {
    submitting.value = false
  }
}

// ── Delete Actions ────────────────────────────────────────────
const confirmDelete = (disease) => {
  diseaseToDelete.value = disease
  deleteModalOpen.value = true
}

const closeDeleteModal = () => {
  if (!submitting.value) {
    deleteModalOpen.value = false
    diseaseToDelete.value = null
  }
}

const handleDelete = async () => {
  if (!diseaseToDelete.value) return

  submitting.value = true
  try {
    const response = await api.deletePenyakit(diseaseToDelete.value.id)
    if (response.success) {
      showToast('success', `Penyakit '${diseaseToDelete.value.kode}' berhasil dihapus.`)
      deleteModalOpen.value = false
      diseaseToDelete.value = null
      await fetchDiseases()
    } else {
      throw new Error(response.message || 'Gagal menghapus penyakit.')
    }
  } catch (err) {
    console.error('Delete disease error:', err)
    showToast('error', err.message || 'Terjadi kesalahan saat menghapus data.')
  } finally {
    submitting.value = false
  }
}

onMounted(() => {
  fetchDiseases()
})
</script>

<style scoped>
.modal-fade-enter-active, .modal-fade-leave-active {
  transition: opacity 0.25s ease-out;
}
.modal-fade-enter-from, .modal-fade-leave-to {
  opacity: 0;
}
@keyframes modal-pop {
  from {
    transform: scale(0.95);
    opacity: 0;
  }
  to {
    transform: scale(1);
    opacity: 1;
  }
}
.animate-modal-pop {
  animation: modal-pop 0.2s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}
.toast-list-enter-active {
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}
.toast-list-leave-active {
  transition: all 0.2s ease-in;
  position: absolute;
}
.toast-list-enter-from {
  transform: translateY(20px) scale(0.9);
  opacity: 0;
}
.toast-list-leave-to {
  transform: translateX(100px);
  opacity: 0;
}
</style>
