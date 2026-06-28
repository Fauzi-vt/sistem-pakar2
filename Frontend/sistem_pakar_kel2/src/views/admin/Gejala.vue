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
            <Menu class="w-5 h-5 text-on-surface" />
          </button>
          <div>
            <h1 class="font-headline-lg text-headline-lg font-bold text-primary leading-tight">Data Gejala</h1>
          </div>
        </div>

        <!-- Right: Actions -->
        <div class="flex items-center gap-stack-md shrink-0">
          <button @click="openCreateModal"
            class="bg-primary-container text-on-tertiary font-label-md py-2.5 px-4 rounded flex items-center justify-center gap-2 hover:bg-primary transition-all cursor-pointer active:scale-95">
            <Plus class="w-5 h-5 text-on-tertiary" />
            <span>Tambah Gejala Baru</span>
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
            <Search class="absolute left-3 top-1/2 -translate-y-1/2 text-on-surface-variant w-5 h-5" />
            <input 
              v-model="searchQuery"
              class="w-full bg-surface-container-lowest border border-outline-variant rounded pl-10 pr-4 py-2 font-body-sm text-on-surface focus:border-secondary focus:ring-1 focus:ring-secondary outline-none transition-all" 
              placeholder="Cari Kode atau Nama Gejala..." 
              type="text"
            />
          </div>
        </div>

        <!-- Data Table Card Container -->
        <section class="bg-surface-container-lowest border border-outline-variant rounded flex flex-col shadow-sm p-4">
          <DataTable :value="filteredGejala" :paginator="true" :rows="10" :loading="loading"
                     class="p-datatable-sm w-full text-sm" responsiveLayout="scroll">
            <template #empty>
              <div class="text-center py-6 text-on-surface-variant italic">
                Tidak ada data gejala ditemukan
              </div>
            </template>
            <Column field="kode" header="Kode Gejala" :sortable="true" style="width: 150px">
              <template #body="slotProps">
                <span class="font-bold text-primary tracking-wider">{{ slotProps.data.kode }}</span>
              </template>
            </Column>
            <Column field="nama" header="Nama Gejala" :sortable="true" style="width: 300px">
              <template #body="slotProps">
                <span class="font-bold text-on-surface">{{ slotProps.data.nama }}</span>
              </template>
            </Column>
            <Column header="Deskripsi Singkat">
              <template #body="slotProps">
                <span class="text-on-surface-variant leading-relaxed">
                  {{ descriptionMap[slotProps.data.kode] || 'Deskripsi gejala klinis.' }}
                </span>
              </template>
            </Column>
            <Column header="Aksi" style="text-align: right; width: 140px">
              <template #body="slotProps">
                <div class="flex items-center justify-end gap-2">
                  <button @click="openEditModal(slotProps.data)"
                          class="text-secondary hover:bg-surface-container-low p-1.5 rounded transition-colors cursor-pointer"
                          title="Edit Gejala">
                    <Edit class="w-5 h-5 text-secondary" />
                  </button>
                  <button @click="confirmDelete(slotProps.data)"
                          class="text-error hover:bg-error-container p-1.5 rounded transition-colors cursor-pointer"
                          title="Hapus Gejala">
                    <Trash2 class="w-5 h-5 text-error" />
                  </button>
                </div>
              </template>
            </Column>
          </DataTable>
        </section>

      </main>

      <!-- Footer -->
      <footer class="border-t border-outline-variant px-6 py-4 bg-surface-container-lowest shrink-0">
        <p class="text-on-surface-variant text-xs text-center">© 2026 Sistem Pakar THT — Kelompok 2 · RS Jasa Kartini. All rights reserved.</p>
      </footer>
    </div>

    <!-- ── FORM DIALOG (Add / Edit) ── -->
    <Transition name="modal-fade">
      <div v-if="modalOpen" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-on-surface/40 backdrop-blur-sm">
        <!-- Dialog Box -->
        <div class="relative w-full max-w-lg bg-surface-container-lowest rounded-xl shadow-2xl overflow-hidden border border-outline-variant animate-modal-pop text-left">
          <!-- Header -->
          <div class="flex items-center justify-between px-6 py-4 border-b border-outline-variant bg-surface-container-low">
            <h3 class="font-bold text-primary flex items-center gap-2">
              <span class="w-2.5 h-2.5 rounded-full bg-secondary"></span>
              <span>{{ isEditing ? 'Edit Data Gejala' : 'Tambah Gejala Baru' }}</span>
            </h3>
            <button @click="modalOpen = false" class="text-on-surface-variant hover:text-on-surface cursor-pointer">
              <X class="w-5 h-5" />
            </button>
          </div>

          <!-- Body Form -->
          <form @submit.prevent="handleSubmitForm" class="p-6 space-y-4 text-sm">
            <!-- Kode Gejala -->
            <div>
              <label class="block font-bold text-xs uppercase tracking-wider mb-1.5 text-on-surface-variant">Kode Gejala <span class="text-error">*</span></label>
              <input
                v-model="kode"
                type="text"
                placeholder="Contoh: G01"
                class="w-full bg-surface-container-lowest border border-outline-variant rounded px-4 py-2 text-on-surface focus:border-secondary focus:ring-1 focus:ring-secondary outline-none transition-all"
                @input="kode = kode.toUpperCase()"
              />
              <p v-if="errors.kode" class="text-xs text-error mt-1">{{ errors.kode }}</p>
              <p v-else class="text-[10px] mt-1 text-on-surface-variant">Gunakan kode unik (contoh: G01, G02, G03)</p>
            </div>

            <!-- Nama Gejala -->
            <div>
              <label class="block font-bold text-xs uppercase tracking-wider mb-1.5 text-on-surface-variant">Nama Gejala <span class="text-error">*</span></label>
              <input
                v-model="nama"
                type="text"
                placeholder="Contoh: Nyeri tenggorokan"
                class="w-full bg-surface-container-lowest border border-outline-variant rounded px-4 py-2 text-on-surface focus:border-secondary focus:ring-1 focus:ring-secondary outline-none transition-all"
              />
              <p v-if="errors.nama" class="text-xs text-error mt-1">{{ errors.nama }}</p>
            </div>

            <!-- Action buttons -->
            <div class="flex items-center justify-end gap-3 pt-4 border-t border-outline-variant/50">
              <button
                type="button"
                @click="modalOpen = false"
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

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useGejalaStore } from '@/stores/gejala.store'
import { useToast } from 'primevue/usetoast'
import { useConfirm } from 'primevue/useconfirm'
import { useForm } from 'vee-validate'
import { gejalaSchema } from '@/schemas/gejala.schema'
import Sidebar from '@/components/Sidebar.vue'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import { Menu, Search, Plus, Trash2, Edit, X } from 'lucide-vue-next'

const sidebarOpen = ref(false)
const searchQuery = ref('')
const toast = useToast()
const confirm = useConfirm()

const gejalaStore = useGejalaStore()
const gejala = computed(() => gejalaStore.gejalaList)
const loading = computed(() => gejalaStore.loading)

const modalOpen = ref(false)
const isEditing = ref(false)
const currentId = ref(null)
const submitting = ref(false)

const { handleSubmit, errors, defineField, setValues, resetForm } = useForm({
  validationSchema: gejalaSchema,
  initialValues: {
    kode: '',
    nama: ''
  }
})

const [kode] = defineField('kode')
const [nama] = defineField('nama')

const descriptionMap = {
  'G01': 'Kenaikan suhu tubuh di atas batas normal (37.5°C) akibat reaksi inflamasi.',
  'G02': 'Rasa nyeri atau tidak nyaman pada tenggorokan saat menelan makanan atau cairan.',
  'G03': 'Suara yang terdengar serak, lemah, atau bahkan hilang akibat peradangan pita suara.',
  'G04': 'Keluarnya lendir berlebih atau sensasi menggelitik pada tenggorokan yang memicu batuk.',
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

const filteredGejala = computed(() => {
  const q = searchQuery.value.trim().toLowerCase()
  if (!q) return gejala.value
  return gejala.value.filter(g =>
    g.kode.toLowerCase().includes(q) || g.nama.toLowerCase().includes(q)
  )
})

const fetchGejala = async () => {
  try {
    await gejalaStore.fetchGejala()
  } catch (err) {
    toast.add({ severity: 'error', summary: 'Gagal', detail: 'Gagal memuat gejala: ' + err.message, life: 3000 })
  }
}

const openCreateModal = () => {
  isEditing.value = false
  currentId.value = null
  resetForm({
    values: {
      kode: '',
      nama: ''
    }
  })
  modalOpen.value = true
}

const openEditModal = (item) => {
  isEditing.value = true
  currentId.value = item.id
  setValues({
    kode: item.kode,
    nama: item.nama
  })
  modalOpen.value = true
}

const handleSubmitForm = handleSubmit(async (values) => {
  submitting.value = true
  try {
    const payload = { 
      kode: values.kode.trim().toUpperCase(), 
      nama: values.nama.trim() 
    }

    if (isEditing.value) {
      const res = await gejalaStore.updateGejala(currentId.value, payload)
      if (res.success) {
        toast.add({ severity: 'success', summary: 'Sukses', detail: `Gejala '${payload.kode}' berhasil diperbarui.`, life: 3000 })
        modalOpen.value = false
        await fetchGejala()
      }
    } else {
      const res = await gejalaStore.createGejala(payload)
      if (res.success) {
        toast.add({ severity: 'success', summary: 'Sukses', detail: `Gejala '${payload.kode}' berhasil ditambahkan.`, life: 3000 })
        modalOpen.value = false
        await fetchGejala()
      }
    }
  } catch (err) {
    toast.add({ severity: 'error', summary: 'Gagal', detail: err.message || 'Terjadi kesalahan sistem.', life: 3000 })
  } finally {
    submitting.value = false
  }
})

const confirmDelete = (item) => {
  confirm.require({
    message: `Apakah Anda yakin ingin menghapus gejala '${item.kode} - ${item.nama}'? Tindakan ini permanen.`,
    header: 'Konfirmasi Hapus',
    icon: 'pi pi-exclamation-triangle',
    rejectClass: 'p-button-secondary p-button-outlined p-button-sm cursor-pointer',
    acceptClass: 'p-button-danger p-button-sm cursor-pointer',
    rejectLabel: 'Batal',
    acceptLabel: 'Hapus',
    accept: async () => {
      try {
        const res = await gejalaStore.deleteGejala(item.id)
        if (res.success) {
          toast.add({ severity: 'success', summary: 'Sukses', detail: `Gejala '${item.kode}' berhasil dihapus.`, life: 3000 })
        }
      } catch (err) {
        toast.add({ severity: 'error', summary: 'Gagal', detail: err.message || 'Gagal menghapus gejala.', life: 3000 })
      }
    }
  })
}

onMounted(fetchGejala)
</script>

<style scoped>
@keyframes modal-pop {
  from { transform: scale(0.98); opacity: 0; }
  to   { transform: scale(1);   opacity: 1; }
}
.animate-modal-pop {
  animation: modal-pop 0.25s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

:deep(.p-datatable-header) {
  background: transparent;
  border: none;
}
:deep(.p-paginator) {
  background: transparent;
  border-top: 1px solid rgba(196, 198, 207, 0.3);
  padding-top: 1rem;
}
</style>
