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
            <Menu class="w-5 h-5 text-on-surface" />
          </button>
          <div class="relative w-full hidden sm:block">
            <Search class="absolute left-3 top-1/2 -translate-y-1/2 text-on-surface-variant w-5 h-5" />
            <input 
              v-model="searchQuery"
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
        <section class="bg-surface-container-lowest border border-outline-variant rounded flex flex-col p-4 shadow-sm">
          <DataTable :value="filteredRiwayat" :paginator="true" :rows="10" :loading="loading"
                     class="p-datatable-sm w-full text-sm" responsiveLayout="scroll">
            <template #empty>
              <div class="text-center py-6 text-on-surface-variant italic">
                Tidak ada data riwayat diagnosa ditemukan
              </div>
            </template>
            <Column field="tanggal" header="Tanggal" :sortable="true" style="width: 160px">
              <template #body="slotProps">
                <span class="text-on-surface-variant font-mono text-xs">
                  {{ formatDate(slotProps.data.tanggal) }}
                </span>
              </template>
            </Column>
            <Column field="name" header="Nama Pasien" :sortable="true" style="width: 200px">
              <template #body="slotProps">
                <span class="font-bold text-primary">{{ slotProps.data.name }}</span>
              </template>
            </Column>
            <Column field="diagnosis" header="Hasil Diagnosis" :sortable="true" style="width: 250px">
              <template #body="slotProps">
                <span class="font-semibold text-on-surface">{{ slotProps.data.diagnosis }}</span>
              </template>
            </Column>
            <Column header="Gejala Terpilih">
              <template #body="slotProps">
                <div class="line-clamp-2 text-on-surface-variant leading-relaxed">
                  {{ slotProps.data.gejala_nama || '-' }}
                </div>
              </template>
            </Column>
            <Column field="probability" header="Probabilitas Posterior" :sortable="true" style="width: 180px">
              <template #body="slotProps">
                <span class="px-2.5 py-1 rounded-full text-xs font-bold border font-mono inline-block" 
                      :class="getBadgeCls(slotProps.data.probability)">
                  {{ (slotProps.data.probability * 100).toFixed(0) }}%
                </span>
              </template>
            </Column>
            <Column header="Aksi" style="text-align: right; width: 140px">
              <template #body="slotProps">
                <div class="flex items-center justify-end gap-2">
                  <button @click="viewDetail(slotProps.data)"
                          class="text-secondary hover:bg-surface-container-low p-1.5 rounded transition-colors cursor-pointer"
                          title="Detail Diagnosa">
                    <Eye class="w-5 h-5 text-secondary" />
                  </button>
                  <button @click="confirmDelete(slotProps.data)"
                          class="text-error hover:bg-error-container p-1.5 rounded transition-colors cursor-pointer"
                          title="Hapus Record">
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

    <!-- ── DETAILS DIALOG ── -->
    <Transition name="fade">
      <div v-if="detailOpen && selectedItem" 
           class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-on-surface/40 backdrop-blur-sm">
        <div class="relative w-full max-w-lg bg-surface-container-lowest rounded-xl shadow-2xl overflow-hidden border border-outline-variant text-left">
          <div class="flex justify-between items-center px-6 py-4 border-b border-outline-variant bg-surface-container-low">
            <h3 class="font-bold text-primary flex items-center gap-2">
              <ClipboardList class="w-5 h-5 text-secondary" />
              <span>Detail Riwayat Diagnosa</span>
            </h3>
            <button @click="detailOpen = false" class="text-on-surface-variant hover:text-on-surface cursor-pointer">
              <X class="w-5 h-5" />
            </button>
          </div>
          <div class="p-6 space-y-4 text-sm max-h-[70vh] overflow-y-auto">
            <div class="grid grid-cols-2 gap-4 border-b border-outline-variant pb-4">
              <div>
                <p class="text-xs font-semibold text-on-surface-variant uppercase">Nama Pasien</p>
                <p class="font-bold text-primary mt-1">{{ selectedItem.name }}</p>
              </div>
              <div>
                <p class="text-xs font-semibold text-on-surface-variant uppercase">Tanggal Periksa</p>
                <p class="font-bold text-primary mt-1">{{ formatDate(selectedItem.tanggal) }}</p>
              </div>
            </div>
            <div class="border-b border-outline-variant pb-4">
              <p class="text-xs font-semibold text-on-surface-variant uppercase">Hasil Diagnosis Penyakit</p>
              <div class="mt-1 flex items-center gap-2">
                <span class="font-bold text-primary text-base">{{ selectedItem.diagnosis }}</span>
                <span class="px-2.5 py-0.5 rounded-full text-xs font-bold border font-mono" 
                      :class="getBadgeCls(selectedItem.probability)">
                  {{ (selectedItem.probability * 100).toFixed(0) }}%
                </span>
              </div>
            </div>
            <div class="border-b border-outline-variant pb-4">
              <p class="text-xs font-semibold text-on-surface-variant uppercase">Gejala Yang Dialami</p>
              <p class="font-medium text-on-surface-variant mt-1 leading-relaxed">{{ selectedItem.gejala_nama || '-' }}</p>
            </div>
            <div>
              <p class="text-xs font-semibold text-on-surface-variant uppercase">Rekomendasi / Solusi Medis</p>
              <p class="font-medium text-on-surface mt-1 leading-relaxed bg-surface-container p-3 rounded border border-outline-variant/50">
                {{ selectedItem.solusi || 'Tidak ada saran medis yang tercatat.' }}
              </p>
            </div>
          </div>
        </div>
      </div>
    </Transition>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRiwayatStore } from '@/stores/riwayat.store'
import { useToast } from 'primevue/usetoast'
import { useConfirm } from 'primevue/useconfirm'
import Sidebar from '@/components/Sidebar.vue'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import { Menu, Search, Trash2, Eye, X, ClipboardList } from 'lucide-vue-next'

const sidebarOpen = ref(false)
const searchQuery = ref('')
const toast = useToast()
const confirm = useConfirm()

const riwayatStore = useRiwayatStore()
const riwayatList = computed(() => riwayatStore.riwayatList)
const loading = computed(() => riwayatStore.loading)

const detailOpen = ref(false)
const selectedItem = ref(null)

const filteredRiwayat = computed(() => {
  const q = searchQuery.value.trim().toLowerCase()
  if (!q) return riwayatList.value
  return riwayatList.value.filter(r => 
    r.name.toLowerCase().includes(q) || r.diagnosis.toLowerCase().includes(q)
  )
})

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

const fetchRiwayat = async () => {
  try {
    await riwayatStore.fetchRiwayat()
  } catch (err) {
    toast.add({ severity: 'error', summary: 'Gagal', detail: 'Gagal memuat riwayat: ' + err.message, life: 3000 })
  }
}

const viewDetail = (item) => {
  selectedItem.value = item
  detailOpen.value = true
}

const confirmDelete = (item) => {
  confirm.require({
    message: `Apakah Anda yakin ingin menghapus record diagnosa '${item.name}'? Tindakan ini permanen.`,
    header: 'Konfirmasi Hapus',
    icon: 'pi pi-exclamation-triangle',
    rejectClass: 'p-button-secondary p-button-outlined p-button-sm cursor-pointer',
    acceptClass: 'p-button-danger p-button-sm cursor-pointer',
    rejectLabel: 'Batal',
    acceptLabel: 'Hapus',
    accept: async () => {
      try {
        const res = await riwayatStore.deleteRiwayat(item.id)
        if (res.success) {
          toast.add({ severity: 'success', summary: 'Sukses', detail: 'Record diagnosa berhasil dihapus.', life: 3000 })
        }
      } catch (err) {
        toast.add({ severity: 'error', summary: 'Gagal', detail: err.message || 'Gagal menghapus record.', life: 3000 })
      }
    }
  })
}

onMounted(fetchRiwayat)
</script>

<style scoped>
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
