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

        <div v-else>
        <!-- PrimeVue DataTable -->
        <DataTable :value="riwayatList" 
                   paginator :rows="10" 
                   dataKey="id" 
                   filterDisplay="menu"
                   v-model:filters="filters"
                   :globalFilterFields="['penyakit']"
                   class="p-datatable-sm"
                   @row-click="onRowClick"
                   rowHover>
          
          <template #header>
            <div class="flex justify-end">
              <span class="p-input-icon-left">
                <i class="material-symbols-outlined absolute top-1/2 -translate-y-1/2 left-3 text-on-surface-variant z-10">search</i>
                <input v-model="filters['global'].value" placeholder="Cari penyakit..." class="border border-outline-variant rounded-lg pl-10 pr-3 py-2 font-body-sm w-full md:w-64 focus:outline-primary" />
              </span>
            </div>
          </template>

          <Column field="tanggal" header="Tanggal" sortable>
            <template #body="{ data }">
              {{ formatDate(data.tanggal) }}
            </template>
          </Column>

          <Column field="penyakit" header="Hasil Diagnosis" sortable>
            <template #body="{ data }">
              <span class="font-bold text-primary">{{ data.penyakit }}</span>
            </template>
          </Column>

          <Column field="persentase" header="Probabilitas" sortable>
            <template #body="{ data }">
              <span class="font-bold" :class="getProbabilityClass(data.persentase)">
                {{ data.persentase.toFixed(2) }}%
              </span>
            </template>
          </Column>

          <Column header="Aksi">
            <template #body="{ data }">
              <button @click.stop="showDetail(data)" class="text-secondary hover:underline font-label-md cursor-pointer">
                Lihat Detail
              </button>
            </template>
          </Column>
        </DataTable>
      </div>
      </div>
    </template>

    <!-- Detail Drawer -->
    <Drawer v-model:visible="isDrawerOpen" position="right" class="w-full md:w-[500px]" :pt="{
      root: { class: 'bg-surface' },
      header: { class: 'bg-surface-container-low border-b border-outline-variant' },
      title: { class: 'font-headline-sm font-bold text-primary' }
    }">
      <template #header>
        <span class="font-headline-sm font-bold text-primary">Detail Diagnosa</span>
      </template>

      <div class="flex flex-col gap-6 py-4" v-if="selectedItem">
        <!-- Card 1: Header (Diagnosis & Tanggal) -->
        <div class="bg-surface-container-lowest border border-outline-variant rounded-xl p-5 shadow-sm">
          <p class="font-label-sm text-on-surface-variant uppercase tracking-wider mb-1">Hasil Analisis</p>
          <h2 class="font-headline-md font-bold text-primary mb-2">{{ selectedItem.penyakit }}</h2>
          <div class="flex items-center gap-2 text-on-surface-variant font-label-sm">
            <span class="material-symbols-outlined text-[16px]">calendar_today</span>
            {{ formatDateTime(selectedItem.tanggal) }}
          </div>
        </div>

        <!-- Card 2: Gejala Dipilih -->
        <div class="bg-surface-container-lowest border border-outline-variant rounded-xl overflow-hidden shadow-sm">
          <div class="bg-surface-container-low px-4 py-3 border-b border-outline-variant flex items-center gap-2">
            <span class="material-symbols-outlined text-secondary text-[18px]">checklist</span>
            <h3 class="font-label-md font-bold text-primary">Gejala yang Dipilih</h3>
          </div>
          <div class="p-4">
            <ul class="flex flex-col gap-2">
              <li v-for="(gejala, idx) in selectedItem.gejala_list" :key="idx" class="flex items-start gap-2">
                <span class="material-symbols-outlined text-[16px] text-tertiary mt-0.5">check_circle</span>
                <span class="font-body-sm text-on-surface">{{ gejala }}</span>
              </li>
            </ul>
          </div>
        </div>

        <!-- Card 3: Hasil Bayes -->
        <div class="bg-surface-container-lowest border border-outline-variant rounded-xl overflow-hidden shadow-sm">
          <div class="bg-surface-container-low px-4 py-3 border-b border-outline-variant flex items-center gap-2">
            <span class="material-symbols-outlined text-secondary text-[18px]">calculate</span>
            <h3 class="font-label-md font-bold text-primary">Probabilitas Diagnosis</h3>
          </div>
          <div class="p-4 flex flex-col items-center">
            <div class="relative w-32 h-32 flex items-center justify-center mb-2">
              <!-- Simple circular representation using CSS border -->
              <div class="absolute inset-0 rounded-full border-[12px] border-surface-container-high"></div>
              <div class="absolute inset-0 rounded-full border-[12px] border-primary"
                   :style="{ clipPath: `polygon(50% 50%, 50% 0%, ${getClipPath(selectedItem.persentase)})` }"></div>
              <div class="absolute inset-2 bg-surface-container-lowest rounded-full flex items-center justify-center">
                <span class="font-headline-md font-black text-primary">{{ selectedItem.persentase.toFixed(2) }}%</span>
              </div>
            </div>
            <p class="font-label-sm text-center text-on-surface-variant max-w-xs">
              Keyakinan sistem terhadap <strong>{{ selectedItem.penyakit }}</strong> berdasarkan perhitungan probabilitas kondisional gejala.
            </p>
          </div>
        </div>

        <!-- Card 4: Penjelasan -->
        <div class="bg-surface-container-lowest border border-outline-variant rounded-xl overflow-hidden shadow-sm">
          <div class="bg-surface-container-low px-4 py-3 border-b border-outline-variant flex items-center gap-2">
            <span class="material-symbols-outlined text-secondary text-[18px]">info</span>
            <h3 class="font-label-md font-bold text-primary">Penjelasan Penyakit</h3>
          </div>
          <div class="p-4">
            <p class="font-body-sm text-on-surface leading-relaxed whitespace-pre-line">{{ selectedItem.deskripsi || 'Informasi tidak tersedia.' }}</p>
          </div>
        </div>

        <!-- Card 5: Saran -->
        <div class="bg-surface-container-lowest border border-outline-variant rounded-xl overflow-hidden shadow-sm">
          <div class="bg-surface-container-low px-4 py-3 border-b border-outline-variant flex items-center gap-2">
            <span class="material-symbols-outlined text-tertiary text-[18px]">medical_services</span>
            <h3 class="font-label-md font-bold text-primary">Saran Penanganan</h3>
          </div>
          <div class="p-4">
            <p class="font-body-sm text-on-surface leading-relaxed whitespace-pre-line">{{ selectedItem.solusi || 'Silakan konsultasikan ke dokter spesialis THT.' }}</p>
          </div>
        </div>

        <!-- Disclaimer Footer -->
        <div class="bg-error-container/30 border border-error-container rounded-lg p-4 mt-2">
          <p class="font-label-sm text-error/90 text-center leading-relaxed">
            <strong>Perhatian:</strong> Hasil diagnosis ini hanya sebagai referensi awal berdasarkan gejala yang Anda masukkan. 
            Segera hubungi fasilitas medis untuk mendapatkan diagnosis klinis dan resep yang tepat.
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
