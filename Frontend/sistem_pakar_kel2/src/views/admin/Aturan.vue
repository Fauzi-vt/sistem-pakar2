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
            <Menu class="w-5 h-5 text-on-surface" />
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
            <Download class="w-5 h-5 text-on-surface" />
            <span>Ekspor CSV</span>
          </button>
          <button @click="openCreateModal"
            class="bg-primary-container text-on-tertiary font-label-md py-2.5 px-4 rounded flex items-center justify-center gap-2 hover:bg-primary transition-all cursor-pointer active:scale-95">
            <Plus class="w-5 h-5 text-on-tertiary" />
            <span>Tambah Relasi</span>
          </button>
        </div>
      </header>

      <!-- Main Canvas -->
      <main class="p-container-padding flex-1 flex flex-col gap-stack-lg">
        
        <!-- Filter & Search Section -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-gutter items-center p-4 bg-surface-container-lowest border border-outline-variant rounded hover:shadow-[0_4px_12px_rgba(26,54,93,0.02)] transition-shadow">
          <!-- Search input -->
          <div class="md:col-span-2 relative w-full">
            <Search class="absolute left-3 top-1/2 -translate-y-1/2 text-on-surface-variant w-5 h-5" />
            <input 
              v-model="searchQuery"
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
        <section class="bg-surface-container-lowest border border-outline-variant rounded flex flex-col p-4 shadow-sm">
          <DataTable :value="filteredRules" :paginator="true" :rows="10" :loading="loading"
                     class="p-datatable-sm w-full text-sm" responsiveLayout="scroll">
            <template #empty>
              <div class="text-center py-6 text-on-surface-variant italic">
                Tidak ada relasi basis pengetahuan ditemukan
              </div>
            </template>
            <Column header="ID Relasi" style="width: 140px">
              <template #body="slotProps">
                <span class="font-bold text-primary tracking-wider">
                  R-{{ slotProps.data.penyakit_kode }}-{{ slotProps.data.gejala_kode }}
                </span>
              </template>
            </Column>
            <Column field="penyakit_nama" header="Penyakit (Hipotesis)" :sortable="true">
              <template #body="slotProps">
                <div>
                  <span class="font-bold text-primary mr-1">[{{ slotProps.data.penyakit_kode }}]</span>
                  <span class="text-on-surface">{{ slotProps.data.penyakit_nama }}</span>
                </div>
              </template>
            </Column>
            <Column field="gejala_nama" header="Gejala (Evidence)" :sortable="true">
              <template #body="slotProps">
                <div>
                  <span class="font-bold text-secondary mr-1">[{{ slotProps.data.gejala_kode }}]</span>
                  <span class="text-on-surface">{{ slotProps.data.gejala_nama }}</span>
                </div>
              </template>
            </Column>
            <Column field="probability" header="Bobot Pakar (CF)" :sortable="true" style="width: 180px">
              <template #body="slotProps">
                <span class="font-mono font-bold text-secondary">
                  {{ slotProps.data.probability.toFixed(2) }}
                </span>
              </template>
            </Column>
            <Column header="Aksi" style="text-align: right; width: 140px">
              <template #body="slotProps">
                <div class="flex items-center justify-end gap-2">
                  <button @click="openEditModal(slotProps.data)"
                          class="text-secondary hover:bg-surface-container-low p-1.5 rounded transition-colors cursor-pointer"
                          title="Edit Relasi">
                    <Edit class="w-5 h-5 text-secondary" />
                  </button>
                  <button @click="confirmDelete(slotProps.data)"
                          class="text-error hover:bg-error-container p-1.5 rounded transition-colors cursor-pointer"
                          title="Hapus Relasi">
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
              <span>{{ isEditing ? 'Edit Relasi Aturan' : 'Tambah Relasi Baru' }}</span>
            </h3>
            <button @click="modalOpen = false" class="text-on-surface-variant hover:text-on-surface cursor-pointer">
              <X class="w-5 h-5" />
            </button>
          </div>

          <!-- Body Form -->
          <form @submit.prevent="handleSubmitForm" class="p-6 space-y-4 text-sm">
            <!-- Penyakit -->
            <div>
              <label class="block font-bold text-xs uppercase tracking-wider mb-1.5 text-on-surface-variant">Penyakit (Hipotesis) <span class="text-error">*</span></label>
              <select
                v-model="penyakit_id"
                class="w-full bg-surface-container-lowest border border-outline-variant rounded px-3 py-2 text-sm text-on-surface focus:border-secondary focus:ring-1 focus:ring-secondary outline-none transition-all cursor-pointer"
              >
                <option value="">-- Pilih Penyakit --</option>
                <option v-for="p in penyakitList" :key="p.id" :value="String(p.id)">
                  [{{ p.kode }}] {{ p.nama }}
                </option>
              </select>
              <p v-if="errors.penyakit_id" class="text-xs text-error mt-1">{{ errors.penyakit_id }}</p>
            </div>

            <!-- Gejala -->
            <div>
              <label class="block font-bold text-xs uppercase tracking-wider mb-1.5 text-on-surface-variant">Gejala (Evidence) <span class="text-error">*</span></label>
              <select
                v-model="gejala_id"
                class="w-full bg-surface-container-lowest border border-outline-variant rounded px-3 py-2 text-sm text-on-surface focus:border-secondary focus:ring-1 focus:ring-secondary outline-none transition-all cursor-pointer"
              >
                <option value="">-- Pilih Gejala --</option>
                <option v-for="g in gejalaList" :key="g.id" :value="String(g.id)">
                  [{{ g.kode }}] {{ g.nama }}
                </option>
              </select>
              <p v-if="errors.gejala_id" class="text-xs text-error mt-1">{{ errors.gejala_id }}</p>
            </div>

            <!-- Bobot Pakar -->
            <div>
              <label class="block font-bold text-xs uppercase tracking-wider mb-1.5 text-on-surface-variant">Bobot Pakar / Probabilitas Kondisional (CF) <span class="text-error">*</span></label>
              <input
                v-model="conditional_probability"
                type="number"
                step="0.01"
                min="0.00"
                max="1.00"
                placeholder="Rentang 0.00 s/d 1.00"
                class="w-full bg-surface-container-lowest border border-outline-variant rounded px-4 py-2 text-on-surface focus:border-secondary focus:ring-1 focus:ring-secondary outline-none transition-all font-mono"
              />
              <p v-if="errors.conditional_probability" class="text-xs text-error mt-1">{{ errors.conditional_probability }}</p>
              <p class="text-[10px] mt-1 text-on-surface-variant">Isikan nilai desimal antara 0.00 sampai 1.00.</p>
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
                <span>{{ isEditing ? 'Simpan Perubahan' : 'Tambah Relasi' }}</span>
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
import { useAturanStore } from '@/stores/aturan.store'
import { usePenyakitStore } from '@/stores/penyakit.store'
import { useGejalaStore } from '@/stores/gejala.store'
import { useToast } from 'primevue/usetoast'
import { useConfirm } from 'primevue/useconfirm'
import { useForm } from 'vee-validate'
import { aturanSchema } from '@/schemas/aturan.schema'
import Sidebar from '@/components/Sidebar.vue'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import { Menu, Search, Download, Plus, Trash2, Edit, X } from 'lucide-vue-next'

const sidebarOpen = ref(false)
const searchQuery = ref('')
const selectedFilterPenyakitId = ref(null)
const toast = useToast()
const confirm = useConfirm()

const aturanStore = useAturanStore()
const penyakitStore = usePenyakitStore()
const gejalaStore = useGejalaStore()

const rules = computed(() => aturanStore.rules)
const loading = computed(() => aturanStore.loading)
const penyakitList = computed(() => penyakitStore.penyakitList)
const gejalaList = computed(() => gejalaStore.gejalaList)

const modalOpen = ref(false)
const isEditing = ref(false)
const currentId = ref(null)
const submitting = ref(false)

const { handleSubmit, errors, defineField, setValues, resetForm } = useForm({
  validationSchema: aturanSchema,
  initialValues: {
    penyakit_id: '',
    gejala_id: '',
    conditional_probability: 0.0
  }
})

const [penyakit_id] = defineField('penyakit_id')
const [gejala_id] = defineField('gejala_id')
const [conditional_probability] = defineField('conditional_probability')

const filteredRules = computed(() => {
  let list = rules.value

  if (selectedFilterPenyakitId.value) {
    list = list.filter(r => r.penyakit_id === selectedFilterPenyakitId.value)
  }

  const q = searchQuery.value.trim().toLowerCase()
  if (!q) return list

  return list.filter(r =>
    r.penyakit_kode.toLowerCase().includes(q) ||
    r.penyakit_nama.toLowerCase().includes(q) ||
    r.gejala_kode.toLowerCase().includes(q) ||
    r.gejala_nama.toLowerCase().includes(q)
  )
})

const fetchInitialData = async () => {
  try {
    await Promise.all([
      penyakitStore.fetchPenyakit(),
      gejalaStore.fetchGejala(),
      aturanStore.fetchRules()
    ])
  } catch (err) {
    toast.add({ severity: 'error', summary: 'Gagal', detail: 'Gagal memuat data: ' + err.message, life: 3000 })
  }
}

const openCreateModal = () => {
  isEditing.value = false
  currentId.value = null
  resetForm({
    values: {
      penyakit_id: '',
      gejala_id: '',
      conditional_probability: 0.0
    }
  })
  modalOpen.value = true
}

const openEditModal = (row) => {
  isEditing.value = true
  currentId.value = row.id
  setValues({
    penyakit_id: String(row.penyakit_id),
    gejala_id: String(row.gejala_id),
    conditional_probability: row.probability
  })
  modalOpen.value = true
}

const handleSubmitForm = handleSubmit(async (values) => {
  submitting.value = true
  try {
    const payload = {
      penyakit_id: parseInt(values.penyakit_id),
      gejala_id: parseInt(values.gejala_id),
      conditional_probability: parseFloat(values.conditional_probability)
    }

    if (isEditing.value) {
      const res = await aturanStore.updateRule(currentId.value, payload)
      if (res.success) {
        toast.add({ severity: 'success', summary: 'Sukses', detail: 'Relasi basis pengetahuan berhasil diperbarui.', life: 3000 })
        modalOpen.value = false
        await aturanStore.fetchRules()
      }
    } else {
      const res = await aturanStore.createRule(payload)
      if (res.success) {
        toast.add({ severity: 'success', summary: 'Sukses', detail: 'Relasi basis pengetahuan berhasil ditambahkan.', life: 3000 })
        modalOpen.value = false
        await aturanStore.fetchRules()
      }
    }
  } catch (err) {
    toast.add({ severity: 'error', summary: 'Gagal', detail: err.message || 'Terjadi kesalahan sistem.', life: 3000 })
  } finally {
    submitting.value = false
  }
})

const confirmDelete = (row) => {
  confirm.require({
    message: `Apakah Anda yakin ingin menghapus relasi R-${row.penyakit_kode}-${row.gejala_kode}? Tindakan ini permanen.`,
    header: 'Konfirmasi Hapus',
    icon: 'pi pi-exclamation-triangle',
    rejectClass: 'p-button-secondary p-button-outlined p-button-sm cursor-pointer',
    acceptClass: 'p-button-danger p-button-sm cursor-pointer',
    rejectLabel: 'Batal',
    acceptLabel: 'Hapus',
    accept: async () => {
      try {
        const res = await aturanStore.deleteRule(row.id)
        if (res.success) {
          toast.add({ severity: 'success', summary: 'Sukses', detail: 'Relasi basis pengetahuan berhasil dihapus.', life: 3000 })
        }
      } catch (err) {
        toast.add({ severity: 'error', summary: 'Gagal', detail: err.message || 'Gagal menghapus relasi.', life: 3000 })
      }
    }
  })
}

const exportToCSV = () => {
  if (filteredRules.value.length === 0) {
    toast.add({ severity: 'error', summary: 'Ekspor Gagal', detail: 'Tidak ada data relasi untuk diekspor.', life: 3000 })
    return
  }
  const headers = ['ID Relasi', 'Penyakit (Hipotesis)', 'Gejala (Evidence)', 'Bobot Pakar (CF)']
  const rows = filteredRules.value.map(row => [
    `R-${row.penyakit_kode}-${row.gejala_kode}`,
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
  toast.add({ severity: 'success', summary: 'Sukses', detail: 'Relasi basis pengetahuan berhasil diekspor ke CSV.', life: 3000 })
}

onMounted(fetchInitialData)
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
