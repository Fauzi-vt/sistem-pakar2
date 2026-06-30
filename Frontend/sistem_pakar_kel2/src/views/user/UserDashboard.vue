<template>
  <UserLayout>
    <template v-if="loading">
      <SkeletonDashboard />
    </template>
    
    <template v-else>
      <AppBreadcrumb :items="[{ label: 'Dashboard' }]" />
      <PageHeader 
        :title="`Selamat Datang, ${userName}`" 
        description="Kelola riwayat kesehatan Telinga, Hidung, dan Tenggorokan Anda dengan bantuan sistem pakar kami." 
      />

      <!-- Quick Stats -->
      <section class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
        <div class="bg-surface-container-lowest border border-outline-variant p-6 rounded-2xl flex items-center gap-4">
          <div class="w-12 h-12 rounded-full bg-primary-container text-on-primary-container flex items-center justify-center shrink-0">
            <span class="material-symbols-outlined">assignment</span>
          </div>
          <div>
            <p class="font-body-sm text-on-surface-variant">Total Diagnosa</p>
            <p class="font-headline-md font-bold text-primary">{{ stats.total_diagnosa }}</p>
          </div>
        </div>
        
        <div class="bg-surface-container-lowest border border-outline-variant p-6 rounded-2xl flex items-center gap-4">
          <div class="w-12 h-12 rounded-full bg-secondary-container text-on-secondary-container flex items-center justify-center shrink-0">
            <span class="material-symbols-outlined">history</span>
          </div>
          <div class="flex-1 min-w-0">
            <p class="font-body-sm text-on-surface-variant">Diagnosa Terakhir</p>
            <p class="font-label-md font-bold text-primary truncate" v-if="stats.last_diagnosa">{{ stats.last_diagnosa.penyakit }}</p>
            <p class="font-label-md font-bold text-outline" v-else>Belum ada</p>
          </div>
        </div>

        <div class="bg-surface-container-lowest border border-outline-variant p-6 rounded-2xl flex items-center gap-4">
          <div class="w-12 h-12 rounded-full bg-tertiary-container text-on-tertiary-container flex items-center justify-center shrink-0">
            <span class="material-symbols-outlined">calendar_today</span>
          </div>
          <div>
            <p class="font-body-sm text-on-surface-variant">Tanggal Bergabung</p>
            <p class="font-label-md font-bold text-primary">{{ joinDate }}</p>
          </div>
        </div>
      </section>

      <!-- Main Content Area -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        <!-- Left Column: Quick Actions & Recent -->
        <div class="lg:col-span-2 flex flex-col gap-6">
          
          <!-- Quick Actions -->
          <section class="bg-surface-container-low border border-outline-variant rounded-2xl p-6">
            <h2 class="font-headline-sm font-bold text-primary mb-4 flex items-center gap-2">
              <span class="material-symbols-outlined text-secondary">bolt</span>
              Aksi Cepat
            </h2>
            <div class="flex flex-col sm:flex-row gap-4">
              <button @click="$router.push('/user/diagnosa')" class="flex-1 bg-primary text-on-primary hover:bg-primary/90 p-4 rounded-xl font-bold flex items-center justify-center gap-2 transition-all shadow-sm active:scale-95 cursor-pointer">
                <span class="material-symbols-outlined">stethoscope</span>
                Mulai Konsultasi Baru
              </button>
              <button @click="$router.push('/user/riwayat')" class="flex-1 bg-surface-container-lowest border border-outline hover:border-primary text-primary p-4 rounded-xl font-bold flex items-center justify-center gap-2 transition-all active:scale-95 cursor-pointer">
                <span class="material-symbols-outlined">receipt_long</span>
                Lihat Semua Riwayat
              </button>
            </div>
          </section>

          <!-- Diagnosis Terakhir -->
          <section class="bg-surface-container-lowest border border-outline-variant rounded-2xl p-6">
            <div class="flex items-center justify-between mb-4">
              <h2 class="font-headline-sm font-bold text-primary">Riwayat Terakhir</h2>
              <button @click="$router.push('/user/riwayat')" class="text-secondary font-label-md hover:underline cursor-pointer">Lihat Semua</button>
            </div>
            
            <EmptyState 
              v-if="recentDiagnoses.length === 0"
              icon="Stethoscope"
              title="Belum ada riwayat"
              description="Mulai diagnosa pertama Anda untuk mendapatkan hasil analisa kesehatan THT."
              actionLabel="Mulai Sekarang"
              @action="$router.push('/user/diagnosa')"
            />
            
            <div v-else class="flex flex-col gap-3">
              <div v-for="item in recentDiagnoses" :key="item.id" class="p-4 rounded-xl border border-outline-variant/60 hover:bg-surface-container-low transition-colors flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                <div>
                  <p class="font-bold text-primary text-lg">{{ item.penyakit }}</p>
                  <div class="flex items-center gap-2 mt-1 font-label-sm text-on-surface-variant">
                    <span class="material-symbols-outlined text-[14px]">calendar_month</span>
                    <span>{{ formatDate(item.tanggal) }}</span>
                  </div>
                </div>
                <div class="flex items-center gap-4">
                  <div class="text-right">
                    <p class="font-label-sm text-on-surface-variant mb-0.5">Probabilitas</p>
                    <p class="font-bold text-lg" :class="item.persentase >= 80 ? 'text-error' : (item.persentase >= 50 ? 'text-tertiary' : 'text-primary')">
                      {{ item.persentase.toFixed(2) }}%
                    </p>
                  </div>
                  <button @click="$router.push('/user/riwayat')" class="w-10 h-10 rounded-full bg-surface-container flex items-center justify-center text-primary hover:bg-secondary-container transition-colors cursor-pointer">
                    <span class="material-symbols-outlined">arrow_forward</span>
                  </button>
                </div>
              </div>
            </div>
          </section>

        </div>

        <!-- Right Column: System Info -->
        <div class="flex flex-col gap-6">
          
          <section class="bg-surface-container-lowest border border-outline-variant rounded-2xl p-6">
            <h2 class="font-headline-sm font-bold text-primary mb-3 flex items-center gap-2">
              <span class="material-symbols-outlined text-tertiary">psychology</span>
              Metode Sistem
            </h2>
            <p class="font-body-sm text-on-surface-variant leading-relaxed">
              Sistem Pakar ini menggunakan algoritma <strong class="text-primary">Teorema Bayes</strong> untuk menghitung probabilitas penyakit berdasarkan gejala yang Anda masukkan. 
              Metode ini mengadopsi cara berpikir probabilistik seorang pakar klinis.
            </p>
          </section>

          <section class="bg-error-container/30 border border-error-container rounded-2xl p-6 text-on-surface">
            <h2 class="font-headline-sm font-bold text-error mb-2 flex items-center gap-2">
              <span class="material-symbols-outlined">warning</span>
              Disclaimer Medis
            </h2>
            <p class="font-body-sm text-on-surface-variant leading-relaxed">
              Hasil diagnosa dari sistem ini bertujuan sebagai <strong>informasi awal</strong> dan edukasi. Hasil ini <strong>TIDAK DAPAT</strong> menggantikan diagnosis langsung, nasihat medis, maupun resep dari dokter spesialis THT. 
              Segera konsultasikan ke fasilitas kesehatan jika gejala memburuk.
            </p>
          </section>
          
        </div>

      </div>
    </template>
  </UserLayout>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth.store'
import { useRiwayatStore } from '@/stores/riwayat.store'
import UserLayout from '@/layouts/UserLayout.vue'
import AppBreadcrumb from '@/components/common/AppBreadcrumb.vue'
import PageHeader from '@/components/common/PageHeader.vue'
import EmptyState from '@/components/common/EmptyState.vue'
import SkeletonDashboard from '@/components/common/SkeletonDashboard.vue'


const authStore    = useAuthStore()
const riwayatStore = useRiwayatStore()

const userName = computed(() => {
  if (!authStore.currentUser?.name) return 'Pengguna'
  return authStore.currentUser.name.split(' ')[0]
})

const joinDate = computed(() => {
  if (!authStore.currentUser?.created_at) return '—'
  return new Date(authStore.currentUser.created_at).toLocaleDateString('id-ID', {
    day: 'numeric', month: 'long', year: 'numeric'
  })
})

// Reaktif: ikut berubah otomatis saat riwayatStore diupdate oleh UserDiagnosa
const loading        = computed(() => riwayatStore.loading)
const recentDiagnoses = computed(() => riwayatStore.recentList)
const stats          = computed(() => ({
  total_diagnosa: riwayatStore.riwayatList.length,
  last_diagnosa:  riwayatStore.riwayatList.length > 0 ? riwayatStore.riwayatList[0] : null
}))

const formatDate = (dateString) => {
  if (!dateString) return '-'
  const dt = new Date(dateString)
  return dt.toLocaleDateString('id-ID', { day: 'numeric', month: 'long', year: 'numeric' })
}

onMounted(async () => {
  if (authStore.currentUser?.id) {
    await riwayatStore.fetchByUser(authStore.currentUser.id)
  }
})
</script>
