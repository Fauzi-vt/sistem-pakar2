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
            <Menu class="w-5 h-5 text-on-surface" />
          </button>
          <div v-if="!showFormView" class="relative w-full hidden sm:block">
            <Search class="absolute left-3 top-1/2 -translate-y-1/2 text-on-surface-variant w-5 h-5" />
            <input 
              v-model="searchQuery"
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
            <Plus class="w-5 h-5 text-on-tertiary" />
            <span>Tambah Penyakit Baru</span>
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
                <Settings class="w-5 h-5 text-on-surface-variant" />
              </div>
              <div class="font-headline-lg text-headline-lg text-primary">{{ diseases.length }}</div>
            </div>

            <!-- Card 2: Status Basis Pengetahuan -->
            <div class="md:col-span-2 bg-surface-container-lowest border border-outline-variant rounded p-stack-md flex flex-col gap-unit hover:shadow-[0_4px_12px_rgba(26,54,93,0.05)] transition-shadow">
              <div class="flex justify-between items-center text-on-surface-variant">
                <span class="font-label-sm text-label-sm uppercase tracking-wider">Status Basis Pengetahuan</span>
                <CheckCircle class="w-5 h-5 text-secondary" />
              </div>
              <div class="font-body-md font-bold text-primary mt-1">Sistem pakar THT saat ini aktif.</div>
              <div class="font-body-sm text-body-sm text-on-surface-variant">
                Pastikan relasi penyakit dan gejala mutakhir.
              </div>
            </div>

          </div>

          <!-- Main Data Table Container -->
          <section class="bg-surface-container-lowest border border-outline-variant rounded flex flex-col p-4 shadow-sm">
            <DataTable :value="filteredDiseases" :paginator="true" :rows="10" :loading="loading"
                       class="p-datatable-sm w-full text-sm" responsiveLayout="scroll">
              <template #empty>
                <div class="text-center py-6 text-on-surface-variant italic">
                  Tidak ada data penyakit ditemukan
                </div>
              </template>
              <Column field="kode" header="Kode" :sortable="true" style="width: 120px">
                <template #body="slotProps">
                  <span class="font-bold text-primary tracking-wider">{{ slotProps.data.kode }}</span>
                </template>
              </Column>
              <Column field="nama" header="Nama Penyakit" :sortable="true" style="width: 250px">
                <template #body="slotProps">
                  <span class="font-bold text-primary">{{ slotProps.data.nama }}</span>
                </template>
              </Column>
              <Column field="deskripsi" header="Deskripsi Singkat">
                <template #body="slotProps">
                  <div class="line-clamp-2 text-on-surface-variant leading-relaxed">
                    {{ slotProps.data.deskripsi || '-' }}
                  </div>
                </template>
              </Column>
              <Column header="Aksi" style="text-align: right; width: 140px">
                <template #body="slotProps">
                  <div class="flex items-center justify-end gap-2">
                    <button @click="openEditModal(slotProps.data)"
                            class="text-secondary hover:bg-surface-container-low p-1.5 rounded transition-colors cursor-pointer"
                            title="Edit Penyakit">
                      <Edit class="w-5 h-5 text-secondary" />
                    </button>
                    <button @click="confirmDelete(slotProps.data)"
                            class="text-error hover:bg-error-container p-1.5 rounded transition-colors cursor-pointer"
                            title="Hapus Penyakit">
                      <Trash2 class="w-5 h-5 text-error" />
                    </button>
                  </div>
                </template>
              </Column>
            </DataTable>
          </section>
        </div>

        <!-- Dedicated Bento Form View -->
        <div v-else class="flex flex-col gap-stack-lg animate-modal-pop">
          <!-- Breadcrumbs / Page Title -->
          <div>
            <div class="flex items-center gap-2 text-on-surface-variant font-label-sm text-label-sm mb-2">
              <button @click="showFormView = false" class="hover:text-primary transition-colors cursor-pointer">Data Penyakit</button>
              <ChevronRight class="w-4 h-4 text-on-surface-variant" />
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
                  <FileEdit v-if="isEditing" class="w-5 h-5 text-primary" />
                  <PlusCircle v-else class="w-5 h-5 text-primary" />
                </div>
                <h2 class="font-headline-sm text-headline-sm text-primary">Informasi Penyakit Utama</h2>
              </div>
              <span class="bg-surface-container-low text-primary font-label-sm text-label-sm px-3 py-1 rounded-full uppercase tracking-wider border border-surface-tint">
                {{ isEditing ? 'Aktif' : 'Draft' }}
              </span>
            </div>

            <!-- Form Fields Container -->
            <form @submit.prevent="handleSubmitForm">
              <div class="p-6 grid grid-cols-1 md:grid-cols-12 gap-gutter">
                
                <!-- Left Column: Primary Identifiers -->
                <div class="md:col-span-5 flex flex-col gap-4">
                  <!-- Kode Penyakit -->
                  <div class="flex flex-col gap-unit">
                    <label class="font-label-md text-label-md text-on-surface" for="kodePenyakit">Kode Penyakit <span class="text-error">*</span></label>
                    <div class="relative">
                      <span class="absolute inset-y-0 left-0 flex items-center pl-3 text-outline">
                        <Hash class="w-5 h-5 text-outline-variant" />
                      </span>
                      <input 
                        v-model="kode"
                        :disabled="isEditing"
                        class="w-full pl-10 pr-4 py-2 bg-surface-container-lowest border border-outline-variant rounded font-body-sm text-body-sm text-on-surface focus:outline-none focus:ring-1 focus:ring-secondary focus:border-secondary transition-all placeholder:text-outline-variant disabled:opacity-50" 
                        id="kodePenyakit" 
                        placeholder="e.g., P01" 
                        type="text"
                        @input="kode = kode.toUpperCase()"
                      />
                    </div>
                    <p v-if="errors.kode" class="text-xs text-error mt-1">{{ errors.kode }}</p>
                    <p v-else class="font-label-sm text-label-sm text-on-surface-variant mt-1">Kode unik untuk identifikasi basis aturan (e.g., P01, P02).</p>
                  </div>

                  <!-- Nama Penyakit -->
                  <div class="flex flex-col gap-unit mt-2">
                    <label class="font-label-md text-label-md text-on-surface" for="namaPenyakit">Nama Penyakit <span class="text-error">*</span></label>
                    <input 
                      v-model="nama"
                      class="w-full px-4 py-2 bg-surface-container-lowest border border-outline-variant rounded font-body-sm text-body-sm text-on-surface focus:outline-none focus:ring-1 focus:ring-secondary focus:border-secondary transition-all placeholder:text-outline-variant" 
                      id="namaPenyakit" 
                      placeholder="Nama diagnosis klinis..." 
                      type="text"
                    />
                    <p v-if="errors.nama" class="text-xs text-error mt-1">{{ errors.nama }}</p>
                  </div>
                </div>

                <!-- Right Column: Detailed Descriptions -->
                <div class="md:col-span-7 flex flex-col gap-4">
                  <!-- Deskripsi Singkat -->
                  <div class="flex flex-col gap-unit">
                    <label class="font-label-md text-label-md text-on-surface" for="deskripsiSingkat">Deskripsi Singkat</label>
                    <textarea 
                      v-model="deskripsi"
                      class="w-full px-4 py-3 bg-surface-container-lowest border border-outline-variant rounded font-body-sm text-body-sm text-on-surface focus:outline-none focus:ring-1 focus:ring-secondary focus:border-secondary transition-all resize-none placeholder:text-outline-variant" 
                      id="deskripsiSingkat" 
                      placeholder="Jelaskan karakteristik umum penyakit..." 
                      rows="3"
                    ></textarea>
                    <p v-if="errors.deskripsi" class="text-xs text-error mt-1">{{ errors.deskripsi }}</p>
                  </div>

                  <!-- Saran Medis / Solusi -->
                  <div class="flex flex-col gap-unit mt-2">
                    <label class="font-label-md text-label-md text-on-surface flex items-center justify-between" for="saranMedis">
                      <span>Saran Medis / Solusi Tindakan <span class="text-error">*</span></span>
                      <Info class="w-4 h-4 text-secondary cursor-help" title="Anjuran yang akan diberikan kepada pasien jika terdiagnosis" />
                    </label>
                    <textarea 
                      v-model="solusi"
                      class="w-full px-4 py-3 bg-surface-container-lowest border border-outline-variant rounded font-body-sm text-body-sm text-on-surface focus:outline-none focus:ring-1 focus:ring-secondary focus:border-secondary transition-all resize-none placeholder:text-outline-variant" 
                      id="saranMedis" 
                      placeholder="Tuliskan rekomendasi pengobatan, anjuran istirahat, atau rujukan spesialis..." 
                      rows="4"
                    ></textarea>
                    <p v-if="errors.solusi" class="text-xs text-error mt-1">{{ errors.solusi }}</p>

                    <!-- Contextual AI Suggestion Chip -->
                    <div class="flex items-center gap-2 mt-2 bg-surface-container-low p-2 rounded border border-outline-variant">
                      <Sparkles class="w-4 h-4 text-secondary" />
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
                  <span v-if="submitting" class="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></span>
                  <span>Simpan</span>
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
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { usePenyakitStore } from '@/stores/penyakit.store'
import { useToast } from 'primevue/usetoast'
import { useConfirm } from 'primevue/useconfirm'
import { useForm } from 'vee-validate'
import { penyakitSchema } from '@/schemas/penyakit.schema'
import Sidebar from '@/components/Sidebar.vue'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import { 
  Menu, Search, Plus, Settings, CheckCircle, ChevronRight, 
  FileEdit, PlusCircle, Hash, Info, Sparkles, Trash2, Edit 
} from 'lucide-vue-next'

const sidebarOpen = ref(false)
const searchQuery = ref('')
const toast = useToast()
const confirm = useConfirm()

const penyakitStore = usePenyakitStore()
const diseases = computed(() => penyakitStore.penyakitList)
const loading = computed(() => penyakitStore.loading)

const showFormView = ref(false)
const isEditing = ref(false)
const currentId = ref(null)
const submitting = ref(false)

const { handleSubmit, errors, defineField, setValues, resetForm } = useForm({
  validationSchema: penyakitSchema,
  initialValues: {
    kode: '',
    nama: '',
    deskripsi: '',
    solusi: ''
  }
})

const [kode] = defineField('kode')
const [nama] = defineField('nama')
const [deskripsi] = defineField('deskripsi')
const [solusi] = defineField('solusi')

const filteredDiseases = computed(() => {
  const q = searchQuery.value.trim().toLowerCase()
  if (!q) return diseases.value
  return diseases.value.filter(d => 
    (d.kode && d.kode.toLowerCase().includes(q)) ||
    (d.nama && d.nama.toLowerCase().includes(q)) ||
    (d.deskripsi && d.deskripsi.toLowerCase().includes(q))
  )
})

const fetchDiseases = async () => {
  try {
    await penyakitStore.fetchPenyakit()
  } catch (err) {
    toast.add({ severity: 'error', summary: 'Gagal', detail: 'Gagal memuat penyakit: ' + err.message, life: 3000 })
  }
}

const openCreateModal = () => {
  isEditing.value = false
  currentId.value = null
  resetForm({
    values: {
      kode: '',
      nama: '',
      deskripsi: '',
      solusi: ''
    }
  })
  showFormView.value = true
}

const openEditModal = (disease) => {
  isEditing.value = true
  currentId.value = disease.id
  setValues({
    kode: disease.kode,
    nama: disease.nama,
    deskripsi: disease.deskripsi || '',
    solusi: disease.solusi || ''
  })
  showFormView.value = true
}

const generateAISuggestion = () => {
  const targetNama = (nama.value || '').trim().toLowerCase()
  if (!targetNama) {
    toast.add({ severity: 'error', summary: 'Gagal', detail: 'Silakan ketik nama penyakit terlebih dahulu sebelum generate saran.', life: 3000 })
    return
  }

  let suggestion
  if (targetNama.includes('otitis')) {
    suggestion = 'Jaga telinga tetap kering, hindari berenang sementara waktu, jangan bersihkan telinga menggunakan cotton bud, dan gunakan obat tetes telinga yang mengandung antibiotik/kortikosteroid sesuai resep.'
  } else if (targetNama.includes('sinusitis')) {
    suggestion = 'Lakukan inhalasi uap air hangat, gunakan nasal spray dekongestan/saline secara berkala, hindari suhu terlalu dingin/berdebu, dan segera hubungi spesialis THT jika gejala menetap lebih dari 10 hari.'
  } else if (targetNama.includes('faringitis') || targetNama.includes('tenggorokan')) {
    suggestion = 'Istirahat cukup, berkumur dengan air garam hangat minimal 3 kali sehari, perbanyak konsumsi cairan hangat, hindari makanan pedas/gorengan, dan minum antibiotik jika diresepkan oleh dokter.'
  } else if (targetNama.includes('rhinitis') || targetNama.includes('alergi')) {
    suggestion = 'Identifikasi dan hindari agen pemicu alergi (debu, bulu hewan, serbuk sari), gunakan antihistamin oral atau semprot hidung kortikosteroid, serta jaga kelembapan udara ruangan.'
  } else if (targetNama.includes('tonsilitis') || targetNama.includes('amandel')) {
    suggestion = 'Istirahat yang cukup, perbanyak minum air hangat, konsumsi makanan bertekstur lunak, kumur antiseptik hangat, dan konsumsi analgesik/antibiotik sesuai anjuran dokter.'
  } else {
    suggestion = 'Konsultasikan dengan dokter spesialis THT untuk pemeriksaan otoskopi/rinoskopi lebih lanjut. Istirahat cukup, konsumsi air putih minimal 2 liter per hari, dan hindari paparan iritan jalan napas.'
  }

  solusi.value = suggestion
  toast.add({ severity: 'success', summary: 'Sukses', detail: 'Rekomendasi klinis standar berhasil digenerate oleh asisten.', life: 3000 })
}

const handleSubmitForm = handleSubmit(async (values) => {
  submitting.value = true
  try {
    const payload = {
      kode: values.kode.trim().toUpperCase(),
      nama: values.nama.trim(),
      deskripsi: (values.deskripsi || '').trim(),
      solusi: values.solusi.trim()
    }

    if (isEditing.value) {
      const response = await penyakitStore.updatePenyakit(currentId.value, payload)
      if (response.success) {
        toast.add({ severity: 'success', summary: 'Sukses', detail: `Penyakit '${payload.kode}' berhasil diperbarui.`, life: 3000 })
        showFormView.value = false
        await fetchDiseases()
      }
    } else {
      const response = await penyakitStore.createPenyakit(payload)
      if (response.success) {
        toast.add({ severity: 'success', summary: 'Sukses', detail: `Penyakit '${payload.kode}' berhasil ditambahkan.`, life: 3000 })
        showFormView.value = false
        await fetchDiseases()
      }
    }
  } catch (err) {
    toast.add({ severity: 'error', summary: 'Gagal', detail: err.message || 'Terjadi kesalahan sistem.', life: 3000 })
  } finally {
    submitting.value = false
  }
})

const confirmDelete = (disease) => {
  confirm.require({
    message: `Apakah Anda yakin ingin menghapus penyakit '${disease.kode} - ${disease.nama}'? Tindakan ini permanen.`,
    header: 'Konfirmasi Hapus',
    icon: 'pi pi-exclamation-triangle',
    rejectClass: 'p-button-secondary p-button-outlined p-button-sm cursor-pointer',
    acceptClass: 'p-button-danger p-button-sm cursor-pointer',
    rejectLabel: 'Batal',
    acceptLabel: 'Hapus',
    accept: async () => {
      try {
        const response = await penyakitStore.deletePenyakit(disease.id)
        if (response.success) {
          toast.add({ severity: 'success', summary: 'Sukses', detail: `Penyakit '${disease.kode}' berhasil dihapus.`, life: 3000 })
        }
      } catch (err) {
        toast.add({ severity: 'error', summary: 'Gagal', detail: err.message || 'Gagal menghapus penyakit.', life: 3000 })
      }
    }
  })
}

onMounted(() => {
  fetchDiseases()
})
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
