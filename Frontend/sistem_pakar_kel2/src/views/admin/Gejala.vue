<template>
  <div class="min-h-screen bg-background text-on-background font-body-md flex relative antialiased">
    <!-- Side Navigation -->
    <Sidebar v-model:isOpen="sidebarOpen" />

    <!-- Main Content Area -->
    <div class="flex-1 flex flex-col min-h-screen lg:ml-64 transition-all duration-300">
      
      <!-- Top Navigation Header -->
      <header class="bg-surface-container-lowest dark:bg-surface-container flex justify-between items-center w-full px-container-padding h-16 sticky top-0 z-40 border-b border-outline-variant">
        <!-- Left: Title -->
        <div class="flex items-center gap-4 w-full lg:w-1/2">
          <button @click="sidebarOpen = !sidebarOpen" 
                  class="lg:hidden flex items-center justify-center p-2 bg-surface-container rounded-lg text-on-surface hover:bg-surface-container-high transition-colors">
            <span class="material-symbols-outlined">menu</span>
          </button>
          <div>
            <h1 class="font-headline-lg text-headline-lg font-bold text-primary leading-tight">Data Gejala</h1>
          </div>
        </div>

        <!-- Right: Actions -->
        <div class="flex items-center gap-stack-md shrink-0">
          <button @click="openCreateModal"
            class="bg-primary-container text-on-tertiary font-label-md py-2.5 px-4 rounded flex items-center justify-center gap-2 hover:bg-primary transition-all cursor-pointer active:scale-95">
            <span class="material-symbols-outlined text-[18px]">add</span>
            Tambah Gejala Baru
          </button>
        </div>
      </header>

      <!-- Main Canvas -->
      <main class="p-container-padding flex-1 flex flex-col gap-stack-lg">
        
        <!-- Description subtitle -->
        <p class="font-body-sm text-body-sm text-on-surface-variant -mt-stack-md">
          Kelola daftar gejala untuk diagnosis penyakit THT.
        </p>

        <!-- Filters & Search Bar -->
        <div class="bg-surface-container-lowest border border-outline-variant rounded p-stack-md shadow-sm flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-4">
          <!-- Search box -->
          <div class="relative w-full sm:w-1/3 min-w-[250px]">
            <span class="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-on-surface-variant">search</span>
            <input 
              v-model="searchQuery"
              @input="currentPage = 1"
              class="w-full bg-surface-container-lowest border border-outline-variant rounded pl-10 pr-4 py-2 font-body-sm text-on-surface focus:border-secondary focus:ring-1 focus:ring-secondary outline-none transition-all" 
              placeholder="Cari Kode atau Nama Gejala..." 
              type="text"
            />
          </div>
          <!-- Filter Actions -->
          <div class="flex gap-stack-sm self-end sm:self-auto">
            <button class="px-4 py-2 border border-outline-variant rounded font-label-md text-label-md text-on-surface hover:bg-surface-container-low transition-colors flex items-center gap-2 cursor-pointer">
              <span class="material-symbols-outlined text-[18px]">filter_list</span> 
              Filter
            </button>
          </div>
        </div>

        <!-- Data Table Card Container -->
        <section class="bg-surface-container-lowest border border-outline-variant rounded flex flex-col shadow-sm">
          <div class="overflow-x-auto w-full">
            <table class="w-full text-left border-collapse">
              <thead>
                <tr class="border-b-2 border-primary bg-background">
                  <th class="p-4 pl-6 font-label-sm text-label-sm text-on-surface-variant uppercase tracking-wider w-36">Kode Gejala</th>
                  <th class="p-4 font-label-sm text-label-sm text-on-surface-variant uppercase tracking-wider w-1/4">Nama Gejala</th>
                  <th class="p-4 font-label-sm text-label-sm text-on-surface-variant uppercase tracking-wider">Deskripsi Singkat</th>
                  <th class="p-4 pr-6 font-label-sm text-label-sm text-on-surface-variant uppercase tracking-wider text-right w-36">Aksi</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-outline-variant/30">
                <tr v-if="loading">
                  <td colspan="4" class="p-12 text-center text-on-surface-variant">
                    <div class="flex items-center justify-center gap-2">
                      <span class="w-4 h-4 border-2 border-t-transparent rounded-full animate-spin border-primary"></span>
                      <span>Memuat data gejala...</span>
                    </div>
                  </td>
                </tr>
                <tr v-else-if="filteredGejala.length === 0">
                  <td colspan="4" class="p-12 text-center text-on-surface-variant italic">Tidak ada data gejala</td>
                </tr>
                
                <tr v-else v-for="item in paginatedGejala" :key="item.id"
                    class="border-b border-outline-variant bg-surface-container-lowest hover:bg-surface-container-low transition-colors group">
                  <!-- Kode -->
                  <td class="p-4 pl-6 font-body-md text-primary font-medium">
                    {{ item.kode }}
                  </td>
                  
                  <!-- Nama -->
                  <td class="p-4 font-body-sm text-on-surface font-semibold">
                    {{ item.nama }}
                  </td>
                  
                  <!-- Deskripsi -->
                  <td class="p-4 font-body-sm text-on-surface-variant leading-relaxed">
                    {{ descriptionMap[item.kode] || 'Deskripsi gejala klinis.' }}
                  </td>
                  
                  <!-- Aksi (with opacity transition on hover) -->
                  <td class="p-4 pr-6 text-right">
                    <div class="flex items-center justify-end gap-2 opacity-0 group-hover:opacity-100 transition-opacity duration-150">
                      <button @click="openEditModal(item)"
                              class="text-primary hover:bg-surface-container p-1 rounded transition-colors cursor-pointer" 
                              title="Edit">
                        <span class="material-symbols-outlined text-[20px]">edit</span>
                      </button>
                      <button @click="confirmDelete(item)"
                              class="text-error hover:bg-error-container rounded p-1 transition-colors cursor-pointer" 
                              title="Hapus">
                        <span class="material-symbols-outlined text-[20px]">delete</span>
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Pagination Section -->
          <div v-if="filteredGejala.length > 0" 
               class="bg-background border-t border-outline-variant p-4 flex items-center justify-between">
            <p class="font-body-sm text-body-sm text-on-surface-variant">
              Menampilkan {{ pageStartIndex }}-{{ pageEndIndex }} dari {{ filteredGejala.length }} gejala
            </p>
            <div class="flex gap-unit">
              <!-- Prev button -->
              <button @click="currentPage > 1 && currentPage--" 
                      :disabled="currentPage === 1"
                      class="w-8 h-8 flex items-center justify-center rounded border border-outline-variant text-on-surface hover:bg-surface-container-low transition-colors disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer">
                <span class="material-symbols-outlined text-[16px]">chevron_left</span>
              </button>
              
              <!-- Page indices -->
              <button v-for="page in totalPages" :key="page"
                      @click="currentPage = page"
                      class="w-8 h-8 flex items-center justify-center rounded font-label-md text-label-md transition-colors cursor-pointer"
                      :class="currentPage === page
                        ? 'bg-primary-container text-on-tertiary font-bold'
                        : 'border border-outline-variant text-on-surface hover:bg-surface-container-low'">
                {{ page }}
              </button>

              <!-- Next button -->
              <button @click="currentPage < totalPages && currentPage++" 
                      :disabled="currentPage === totalPages"
                      class="w-8 h-8 flex items-center justify-center rounded border border-outline-variant text-on-surface hover:bg-surface-container-low transition-colors disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer">
                <span class="material-symbols-outlined text-[16px]">chevron_right</span>
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
              {{ isEditing ? 'Edit Data Gejala' : 'Tambah Gejala Baru' }}
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

            <!-- Kode Gejala -->
            <div>
              <label class="block font-bold text-xs uppercase tracking-wider mb-1.5 text-on-surface-variant">Kode Gejala <span class="text-error">*</span></label>
              <input
                v-model="formData.kode"
                type="text"
                required
                placeholder="Contoh: G01"
                class="w-full bg-surface-container-lowest border border-outline-variant rounded px-4 py-2 text-on-surface focus:border-secondary focus:ring-1 focus:ring-secondary outline-none transition-all"
                @input="formData.kode = formData.kode.toUpperCase()"
              />
              <p class="text-[10px] mt-1 text-on-surface-variant">Gunakan kode unik (contoh: G01, G02, G03)</p>
            </div>

            <!-- Nama Gejala -->
            <div>
              <label class="block font-bold text-xs uppercase tracking-wider mb-1.5 text-on-surface-variant">Nama Gejala <span class="text-error">*</span></label>
              <input
                v-model="formData.nama"
                type="text"
                required
                placeholder="Contoh: Nyeri tenggorokan"
                class="w-full bg-surface-container-lowest border border-outline-variant rounded px-4 py-2 text-on-surface focus:border-secondary focus:ring-1 focus:ring-secondary outline-none transition-all"
              />
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
                <span>{{ isEditing ? 'Simpan Perubahan' : 'Tambah Gejala' }}</span>
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

            <h3 class="font-bold text-lg mb-2 text-primary">Hapus Gejala?</h3>
            <p class="text-sm mb-6 leading-relaxed text-on-surface-variant">
              Apakah Anda yakin ingin menghapus gejala <strong class="text-primary">{{ gejalaToDelete?.kode }} - {{ gejalaToDelete?.nama }}</strong>? 
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
const gejala = ref([])
const searchQuery = ref('')
const loading = ref(false)
const error = ref(null)

// Pagination State
const currentPage = ref(1)
const itemsPerPage = ref(5) // Paginate 5 items per page

// Form Modal State
const modalOpen = ref(false)
const isEditing = ref(false)
const submitting = ref(false)
const formError = ref(null)
const formData = ref({ id: '', kode: '', nama: '' })

// Delete Modal State
const deleteModalOpen = ref(false)
const gejalaToDelete = ref(null)

// Toast System State
const toasts = ref([])
let toastIdCounter = 0

// Clinical Descriptions local map matching ICD-10 symptoms list
const descriptionMap = {
  'G01': 'Rasa nyeri atau iritasi pada tenggorokan, seringkali memburuk saat menelan.',
  'G02': 'Peningkatan suhu tubuh di atas normal (37.5°C).',
  'G03': 'Tidur mendengkur akibat adanya hambatan aliran udara di jalan napas.',
  'G04': 'Peningkatan suhu tubuh berulang dalam jangka waktu tertentu.',
  'G05': 'Aroma tidak sedap yang keluar dari rongga mulut.',
  'G06': 'Pembengkakan pada kelenjar getah bening di area leher.',
  'G07': 'Sensasi tekanan atau sumbatan di dalam rongga telinga.',
  'G08': 'Reaksi bersin berulang akibat iritasi pada saluran hidung.',
  'G09': 'Keluarnya cairan hidung yang berwarna bening dan encer.',
  'G10': 'Sensasi hidung mampet yang mengganggu pernapasan normal.',
  'G11': 'Sensasi gatal yang mengganggu pada area mukosa hidung.',
  'G12': 'Sensasi gatal atau mengganjal pada area mata.',
  'G13': 'Keluarnya cairan hidung yang kental dan berwarna kuning kehijauan.',
  'G14': 'Rasa tertekan atau nyeri pada area pipi, dahi, atau sekitar mata.',
  'G15': 'Rasa sakit atau tidak nyaman pada bagian dalam telinga.',
  'G16': 'Keluarnya cairan bening, keruh, atau nanah dari liang telinga.',
  'G17': 'Penurunan kemampuan mendengar atau tuli sementara/permanen.',
  'G18': 'Sensasi gatal yang mengganggu di dalam liang telinga.',
  'G19': 'Keluarnya darah segar atau kecokelatan dari liang telinga.',
  'G20': 'Pembengkakan atau inflamasi pada daun telinga atau liang telinga.'
}

// ── Computed ──────────────────────────────────────────────────
const filteredGejala = computed(() => {
  const q = searchQuery.value.trim().toLowerCase()
  if (!q) return gejala.value
  return gejala.value.filter(g =>
    g.kode.toLowerCase().includes(q) || g.nama.toLowerCase().includes(q)
  )
})

// ── Computed: pagination logic ────────────────────────────────
const totalPages = computed(() => {
  return Math.ceil(filteredGejala.value.length / itemsPerPage.value) || 1
})

const paginatedGejala = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value
  const end = start + itemsPerPage.value
  return filteredGejala.value.slice(start, end)
})

const pageStartIndex = computed(() => {
  if (filteredGejala.value.length === 0) return 0
  return (currentPage.value - 1) * itemsPerPage.value + 1
})

const pageEndIndex = computed(() => {
  return Math.min(currentPage.value * itemsPerPage.value, filteredGejala.value.length)
})

// ── API ───────────────────────────────────────────────────────
const fetchGejala = async () => {
  loading.value = true
  error.value   = null
  try {
    const res = await api.getGejala()
    gejala.value = res.success ? res.data : []
  } catch (err) {
    error.value = err.message
    showToast('error', err.message)
  } finally {
    loading.value = false
  }
}

// ── Toast ─────────────────────────────────────────────────────
const showToast = (type, message) => {
  const id = toastIdCounter++
  toasts.value.push({ id, type, message })
  setTimeout(() => removeToast(id), 4500)
}
const removeToast = (id) => { toasts.value = toasts.value.filter(t => t.id !== id) }

// ── Modal helpers ─────────────────────────────────────────────
const openCreateModal = () => {
  isEditing.value = false
  formError.value = null
  formData.value  = { id: '', kode: '', nama: '' }
  modalOpen.value = true
}

const openEditModal = (item) => {
  isEditing.value = true
  formError.value = null
  formData.value  = { id: item.id, kode: item.kode, nama: item.nama }
  modalOpen.value = true
}

const closeModal = () => { if (!submitting.value) modalOpen.value = false }

// ── Submit ────────────────────────────────────────────────────
const handleSubmit = async () => {
  if (!formData.value.kode.trim() || !formData.value.nama.trim()) {
    formError.value = 'Kode dan nama gejala wajib diisi.'
    return
  }
  submitting.value = true
  formError.value  = null
  try {
    const payload = { kode: formData.value.kode.trim().toUpperCase(), nama: formData.value.nama.trim() }
    const res = isEditing.value
      ? await api.updateGejala(formData.value.id, payload)
      : await api.createGejala(payload)
    if (res.success) {
      showToast('success', isEditing.value ? `Gejala '${payload.kode}' berhasil diperbarui.` : `Gejala '${payload.kode}' berhasil ditambahkan.`)
      modalOpen.value = false
      await fetchGejala()
    }
  } catch (err) {
    formError.value = err.message
    showToast('error', err.message)
  } finally {
    submitting.value = false
  }
}

// ── Delete ────────────────────────────────────────────────────
const confirmDelete     = (item) => { gejalaToDelete.value = item; deleteModalOpen.value = true }
const closeDeleteModal  = () => { if (!submitting.value) { deleteModalOpen.value = false; gejalaToDelete.value = null } }

const handleDelete = async () => {
  if (!gejalaToDelete.value) return
  submitting.value = true
  try {
    const res = await api.deleteGejala(gejalaToDelete.value.id)
    if (res.success) {
      showToast('success', `Gejala '${gejalaToDelete.value.kode}' berhasil dihapus.`)
      deleteModalOpen.value = false
      gejalaToDelete.value  = null
      await fetchGejala()
    }
  } catch (err) {
    showToast('error', err.message)
  } finally {
    submitting.value = false
  }
}

onMounted(fetchGejala)
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
</style>
