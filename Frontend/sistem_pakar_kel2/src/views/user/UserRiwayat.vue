<template>
  <UserLayout>
    <AppBreadcrumb :items="[{ label: 'Dashboard', to: '/user/dashboard' }, { label: 'Riwayat Diagnosa' }]" />
    <PageHeader 
      title="Riwayat Diagnosa" 
      description="Lihat kembali hasil konsultasi dan diagnosis THT yang pernah Anda lakukan sebelumnya." 
    />

    <template v-if="loading">
      <SkeletonRiwayat />
    </template>
    
    <template v-else>
      <div class="bg-surface-container-lowest border border-outline-variant rounded-2xl p-6 mb-8">
        <EmptyState 
          v-if="riwayatList.length === 0"
          icon="History"
          title="Belum ada riwayat"
          description="Anda belum pernah melakukan diagnosa. Mulai konsultasi pertama Anda sekarang."
          actionLabel="Mulai Diagnosa"
          @action="$router.push('/user/diagnosa')"
        />

        <div v-else class="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
          <!-- PrimeVue DataTable -->
          <DataTable :value="riwayatList" 
                     paginator :rows="10" 
                     dataKey="id" 
                     filterDisplay="menu"
                     v-model:filters="filters"
                     :globalFilterFields="['penyakit']"
                     class="p-datatable-sm elegant-table"
                     @row-click="onRowClick"
                     rowHover>
            
            <template #header>
              <div class="flex justify-between items-center px-2 py-2">
                <h3 class="text-lg font-bold text-slate-800">Daftar Riwayat</h3>
                <span class="p-input-icon-left relative">
                  <i class="material-symbols-outlined absolute top-1/2 -translate-y-1/2 left-3 text-slate-400 z-10 text-[20px]">search</i>
                  <input v-model="filters['global'].value" placeholder="Cari penyakit..." class="border border-slate-300 rounded-full pl-10 pr-4 py-2 text-sm w-full md:w-72 focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-transparent transition-all shadow-sm" />
                </span>
              </div>
            </template>

            <Column field="tanggal" header="Tanggal" sortable style="width: 20%">
              <template #body="{ data }">
                <div class="flex items-center gap-2 text-slate-600 font-medium">
                  <span class="material-symbols-outlined text-[16px] text-slate-400">calendar_today</span>
                  {{ formatDate(data.tanggal) }}
                </div>
              </template>
            </Column>

            <Column field="penyakit" header="Hasil Diagnosis" sortable style="width: 40%">
              <template #body="{ data }">
                <span class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-teal-50 border border-teal-100 text-teal-700 font-bold text-sm">
                  🩺 {{ data.penyakit }}
                </span>
              </template>
            </Column>

            <Column field="persentase" header="Probabilitas" sortable style="width: 25%">
              <template #body="{ data }">
                <div class="flex items-center gap-2">
                  <span class="font-bold text-sm" :class="getProbabilityClass(data.persentase)">
                    {{ Number(data.persentase || 0).toFixed(2) }}%
                  </span>
                  <div class="w-16 h-1.5 bg-slate-100 rounded-full overflow-hidden">
                    <div class="h-full rounded-full transition-all duration-500" 
                         :class="getProbabilityBgClass(data.persentase)"
                         :style="{ width: `${Number(data.persentase || 0)}%` }">
                    </div>
                  </div>
                </div>
              </template>
            </Column>

            <Column header="Aksi" style="width: 15%">
              <template #body="{ data }">
                <button @click.stop="showDetail(data)" class="flex items-center gap-1.5 px-4 py-1.5 bg-white border border-slate-300 hover:bg-slate-50 text-slate-700 hover:text-teal-600 rounded-lg text-sm font-semibold transition-colors shadow-sm">
                  <span class="material-symbols-outlined text-[16px]">visibility</span>
                  Detail
                </button>
              </template>
            </Column>
          </DataTable>
        </div>
      </div>
    </template>

    <!-- Detail Drawer -->
    <Drawer v-model:visible="isDrawerOpen" position="right" class="w-full md:w-[500px]" :pt="{
      root: { class: 'bg-slate-50' },
      header: { class: 'bg-white border-b border-slate-200 px-6 py-4' },
      title: { class: 'text-xl font-bold text-slate-800' }
    }">
      <template #header>
        <div class="flex items-center gap-2">
          <span class="material-symbols-outlined text-teal-600">assignment</span>
          <span class="text-lg font-bold text-slate-800">Detail Diagnosa</span>
        </div>
      </template>

      <div class="flex flex-col gap-5 p-2" v-if="selectedItem">
        <!-- Card 1: Header (Diagnosis & Tanggal) -->
        <div class="bg-white border border-slate-200 rounded-2xl p-6 shadow-sm relative overflow-hidden">
          <div class="absolute top-0 left-0 w-1.5 h-full bg-teal-500"></div>
          <p class="text-xs font-semibold text-slate-500 uppercase tracking-widest mb-1">Hasil Analisis</p>
          <h2 class="text-2xl font-bold text-slate-800 mb-3 flex items-center gap-2">
            {{ selectedItem.penyakit }}
          </h2>
          <div class="flex items-center gap-2 text-slate-500 text-sm font-medium">
            <span class="material-symbols-outlined text-[18px]">calendar_today</span>
            {{ formatDateTime(selectedItem.tanggal) }}
          </div>
        </div>

        <!-- Card 2: Gejala Dipilih -->
        <div class="bg-white border border-slate-200 rounded-2xl overflow-hidden shadow-sm">
          <div class="bg-slate-50/80 px-5 py-3.5 border-b border-slate-200 flex items-center gap-2.5">
            <span class="material-symbols-outlined text-teal-600 text-[20px]">checklist</span>
            <h3 class="font-bold text-slate-800">Gejala yang Dialami</h3>
          </div>
          <div class="p-5">
            <ul class="flex flex-col gap-3">
              <li v-for="(gejala, idx) in selectedItem.gejala_list" :key="idx" class="flex items-start gap-3">
                <span class="material-symbols-outlined text-[20px] text-teal-500 mt-0.5">check_circle</span>
                <span class="text-slate-700 leading-relaxed">{{ gejala }}</span>
              </li>
            </ul>
          </div>
        </div>

        <!-- Card 3: Hasil Bayes -->
        <div class="bg-white border border-slate-200 rounded-2xl overflow-hidden shadow-sm">
          <div class="bg-slate-50/80 px-5 py-3.5 border-b border-slate-200 flex items-center gap-2.5">
            <span class="material-symbols-outlined text-teal-600 text-[20px]">analytics</span>
            <h3 class="font-bold text-slate-800">Tingkat Probabilitas</h3>
          </div>
          <div class="p-6">
            <div class="flex items-center justify-between mb-2">
              <span class="text-slate-600 font-medium">Tingkat Keyakinan Sistem</span>
              <span class="text-2xl font-black" :class="getProbabilityClass(selectedItem.persentase)">
                {{ Number(selectedItem.persentase || 0).toFixed(2) }}%
              </span>
            </div>
            <div class="w-full h-3 bg-slate-100 rounded-full overflow-hidden mb-4">
              <div class="h-full rounded-full transition-all duration-1000 ease-out" 
                   :class="getProbabilityBgClass(selectedItem.persentase)"
                   :style="{ width: `${Number(selectedItem.persentase || 0)}%` }">
              </div>
            </div>
            <p class="text-sm text-slate-500 text-center leading-relaxed bg-slate-50 p-3 rounded-xl">
              Tingkat keyakinan bahwa diagnosis mengarah pada <strong>{{ selectedItem.penyakit }}</strong> berdasarkan perhitungan Teorema Bayes.
            </p>
          </div>
        </div>

        <!-- Card 4: Penjelasan -->
        <div class="bg-white border border-slate-200 rounded-2xl overflow-hidden shadow-sm">
          <div class="bg-slate-50/80 px-5 py-3.5 border-b border-slate-200 flex items-center gap-2.5">
            <span class="material-symbols-outlined text-teal-600 text-[20px]">info</span>
            <h3 class="font-bold text-slate-800">Informasi Penyakit</h3>
          </div>
          <div class="p-5">
            <p class="text-slate-700 leading-relaxed whitespace-pre-line">{{ selectedItem.deskripsi || 'Informasi deskripsi penyakit tidak tersedia.' }}</p>
          </div>
        </div>

        <!-- Card 5: Saran -->
        <div class="bg-white border border-slate-200 rounded-2xl overflow-hidden shadow-sm">
          <div class="bg-teal-50/50 px-5 py-3.5 border-b border-teal-100 flex items-center gap-2.5">
            <span class="material-symbols-outlined text-teal-600 text-[20px]">medical_services</span>
            <h3 class="font-bold text-teal-800">Saran Penanganan</h3>
          </div>
          <div class="p-5 bg-teal-50/30">
            <p class="text-teal-900 leading-relaxed whitespace-pre-line">{{ selectedItem.solusi || 'Silakan konsultasikan lebih lanjut ke dokter spesialis THT.' }}</p>
          </div>
        </div>

        <!-- Disclaimer Footer -->
        <div class="bg-amber-50 border border-amber-200 rounded-xl p-4 mt-2">
          <p class="text-sm text-amber-800 text-center leading-relaxed">
            <strong class="font-semibold block mb-1">⚠️ Perhatian</strong>
            Hasil diagnosis ini hanya sebagai skrining awal. Segera hubungi dokter atau fasilitas kesehatan untuk mendapatkan diagnosis klinis yang pasti.
          </p>
        </div>

      </div>
    </Drawer>

  </UserLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { FilterMatchMode } from '@primevue/core/api'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Drawer from 'primevue/drawer'
import UserLayout from '@/layouts/UserLayout.vue'
import AppBreadcrumb from '@/components/common/AppBreadcrumb.vue'
import PageHeader from '@/components/common/PageHeader.vue'
import EmptyState from '@/components/common/EmptyState.vue'
import SkeletonRiwayat from '@/components/common/SkeletonRiwayat.vue'
import { useAuthStore } from '@/stores/auth.store'
import { riwayatApi } from '@/services/api/riwayat.js'

const authStore = useAuthStore()
const loading = ref(true)
const riwayatList = ref([])
const isDrawerOpen = ref(false)
const selectedItem = ref(null)

const filters = ref({
  global: { value: null, matchMode: FilterMatchMode.CONTAINS }
})

const fetchRiwayat = async () => {
  loading.value = true
  try {
    if (authStore.currentUser?.id) {
      const res = await riwayatApi.getByUser(authStore.currentUser.id)
      if (res.success) {
        riwayatList.value = res.data.map(item => ({
          id: item.id,
          tanggal: item.tanggal,
          penyakit: item.penyakit,
          persentase: item.persentase,
          gejala_list: item.gejala ? item.gejala.split(', ') : [],
          deskripsi: item.deskripsi,
          solusi: item.solusi
        }))
      }
    }
  } catch (error) {
    console.error('Failed fetching riwayat', error)
  } finally {
    loading.value = false
  }
}

const formatDate = (dateString) => {
  if (!dateString) return '-'
  const dt = new Date(dateString)
  return dt.toLocaleDateString('id-ID', { day: 'numeric', month: 'short', year: 'numeric' })
}

const formatDateTime = (dateString) => {
  if (!dateString) return '-'
  const dt = new Date(dateString)
  return dt.toLocaleDateString('id-ID', { day: 'numeric', month: 'long', year: 'numeric', hour: '2-digit', minute: '2-digit' })
}

const getProbabilityClass = (val) => {
  if (val >= 80) return 'text-error'
  if (val >= 50) return 'text-tertiary'
  return 'text-primary'
}

const getProbabilityBgClass = (val) => {
  if (val >= 80) return 'bg-error'
  if (val >= 50) return 'bg-tertiary'
  return 'bg-primary'
}

const showDetail = (data) => {
  selectedItem.value = data
  isDrawerOpen.value = true
}

const onRowClick = (event) => {
  showDetail(event.data)
}

const getClipPath = (percentage) => {
  // A rough approximation for circular reveal clip-path based on percentage.
  // In a real app you'd use an SVG circle with stroke-dasharray for perfect precision.
  const angle = (percentage / 100) * 360
  if (angle <= 45) return '100% 0%'
  if (angle <= 135) return '100% 100%'
  if (angle <= 225) return '0% 100%'
  if (angle <= 315) return '0% 0%'
  return '50% 0%' // 100%
}

onMounted(() => {
  fetchRiwayat()
})
</script>

<style scoped>
:deep(.elegant-table .p-datatable-thead > tr > th) {
  background-color: #f8fafc;
  color: #475569;
  font-weight: 700;
  border-bottom: 1px solid #e2e8f0;
  border-top: none;
  padding: 1rem 1.5rem;
}

:deep(.elegant-table .p-datatable-tbody > tr > td) {
  border-bottom: 1px solid #f1f5f9;
  padding: 1rem 1.5rem;
}

:deep(.elegant-table .p-datatable-tbody > tr:last-child > td) {
  border-bottom: none;
}

:deep(.elegant-table .p-datatable-wrapper) {
  border: none;
}
</style>
