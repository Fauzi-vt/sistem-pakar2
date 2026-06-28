<template>
  <div class="min-h-screen bg-background text-on-background font-body-md flex relative antialiased">
    <!-- Side Navigation -->
    <Sidebar v-model:isOpen="sidebarOpen" />

    <!-- Main Content Area -->
    <div class="flex-1 flex flex-col min-h-screen lg:ml-64 transition-all duration-300">
      
      <!-- Top Navigation Header -->
      <header class="bg-surface-container-lowest dark:bg-surface-container flex justify-between items-center w-full px-container-padding h-16 sticky top-0 z-40 border-b border-outline-variant">
        <!-- Left Part: Toggle and Search -->
        <div class="flex items-center gap-4 w-full lg:w-1/3">
          <button @click="sidebarOpen = !sidebarOpen" 
                  class="lg:hidden flex items-center justify-center p-2 bg-surface-container rounded-lg text-on-surface hover:bg-surface-container-high transition-colors">
            <span class="material-symbols-outlined">menu</span>
          </button>
          <div class="relative w-full hidden sm:block">
            <span class="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-on-surface-variant">search</span>
            <input v-model="searchQuery" class="w-full bg-surface-container-lowest border border-outline-variant rounded pl-10 pr-4 py-2 font-body-sm text-on-surface focus:border-secondary focus:ring-1 focus:ring-secondary outline-none transition-all" placeholder="Cari diagnosa atau pasien..." type="text">
          </div>
        </div>

        <!-- Right Part: Actions & Profile -->
        <div class="flex items-center gap-stack-md relative">
          <!-- Notification Bell -->
          <div class="relative">
            <button @click="notificationMenuOpen = !notificationMenuOpen; profileMenuOpen = false" 
                    class="text-on-surface-variant hover:bg-surface-container-low p-2 rounded transition-colors duration-200 cursor-pointer active:opacity-80 relative flex items-center justify-center"
                    title="Notifikasi">
              <span class="material-symbols-outlined">notifications</span>
              <!-- Unread badge -->
              <span v-if="logs.length > 0" class="absolute top-1.5 right-1.5 w-2 h-2 bg-error rounded-full"></span>
            </button>
            
            <!-- Click Outside Overlay for Notification -->
            <div v-if="notificationMenuOpen" @click="notificationMenuOpen = false" class="fixed inset-0 z-40"></div>
            
            <!-- Notification Dropdown -->
            <Transition name="fade">
              <div v-if="notificationMenuOpen" class="absolute right-0 mt-2 w-80 bg-surface-container-lowest border border-outline-variant rounded-lg shadow-xl z-50 overflow-hidden text-left">
                <div class="px-4 py-3 border-b border-outline-variant bg-surface-container-low flex justify-between items-center">
                  <span class="font-bold text-sm text-primary">Notifikasi</span>
                  <span class="text-xs text-secondary font-medium">{{ logs.length }} Baru</span>
                </div>
                <div class="divide-y divide-outline-variant/30 max-h-80 overflow-y-auto">
                  <div v-if="logs.length === 0" class="px-4 py-6 text-center text-xs text-on-surface-variant italic">
                    Tidak ada notifikasi baru
                  </div>
                  <div v-else v-for="(log, idx) in logs" :key="idx" 
                       class="px-4 py-3 hover:bg-surface-container-low transition-colors flex gap-3 cursor-pointer"
                       @click="router.push('/admin/riwayat'); notificationMenuOpen = false">
                    <div class="p-1 rounded h-fit shrink-0 mt-0.5" :class="log.icon_cls">
                      <span class="material-symbols-outlined text-sm">{{ log.icon }}</span>
                    </div>
                    <div class="flex-1 min-w-0">
                      <p class="text-xs font-bold text-primary truncate">{{ log.title }}</p>
                      <p class="text-[11px] text-on-surface-variant leading-relaxed mt-0.5">{{ log.message }}</p>
                      <p class="text-[10px] text-outline mt-1">{{ log.time }}</p>
                    </div>
                  </div>
                </div>
                <div class="border-t border-outline-variant p-2 text-center bg-surface-container-low">
                  <a @click="router.push('/admin/riwayat'); notificationMenuOpen = false" class="text-xs font-bold text-secondary hover:underline cursor-pointer block py-1">Lihat Semua Riwayat</a>
                </div>
              </div>
            </Transition>
          </div>

          <!-- Settings Button -->
          <button @click="router.push('/admin/pengaturan')" 
                  class="text-on-surface-variant hover:bg-surface-container-low p-2 rounded transition-colors duration-200 cursor-pointer active:opacity-80 flex items-center justify-center"
                  title="Pengaturan">
            <span class="material-symbols-outlined">settings</span>
          </button>

          <!-- Profile Dropdown -->
          <div class="relative">
            <button @click="profileMenuOpen = !profileMenuOpen; notificationMenuOpen = false" 
                    class="w-8 h-8 rounded-full overflow-hidden border border-outline-variant hover:border-secondary transition-all cursor-pointer active:scale-95 flex items-center justify-center"
                    title="Menu Profil">
              <img alt="Medical professional profile picture" class="w-full h-full object-cover" src="https://lh3.googleusercontent.com/aida-public/AB6AXuAWoTwRpq8rwHSTU8reRlgKRBb7Tf8kV8t1VUE4fvM26yNC6MXOhO6Tm1gNontoTHWXYVG6snsrEbPirYlDmEubo5uVWTDUg-zGhfC0aFJ64DrphSP--FKm8rikvYkNwbnZMz3jy5cnmviRio9u8k7foQY8i0tCTdBSTZgP9PqFjjXuWTzR-x3e_5md1hzOECJNB2qysMU_IJc4ECf6-CGkDL-NxOA2_Vt4VTJ003gjVOYTziW7T9M-lD4Qwypg4MSCStzTXpRYhFkl">
            </button>
            
            <!-- Click Outside Overlay for Profile -->
            <div v-if="profileMenuOpen" @click="profileMenuOpen = false" class="fixed inset-0 z-40"></div>
            
            <!-- Profile Dropdown Menu -->
            <Transition name="fade">
              <div v-if="profileMenuOpen" class="absolute right-0 mt-2 w-64 bg-surface-container-lowest border border-outline-variant rounded-lg shadow-xl z-50 overflow-hidden text-left">
                <!-- User Card Header -->
                <div class="p-4 border-b border-outline-variant bg-surface-container-low flex items-center gap-3">
                  <div class="w-10 h-10 rounded-full bg-primary text-on-tertiary flex items-center justify-center font-bold text-sm shrink-0">
                    {{ (authStore.currentUser?.name || 'A').charAt(0).toUpperCase() }}
                  </div>
                  <div class="min-w-0">
                    <p class="text-sm font-bold text-primary truncate leading-tight">{{ authStore.currentUser?.name || 'Admin' }}</p>
                    <p class="text-xs text-on-surface-variant truncate mt-0.5">{{ authStore.currentUser?.email || 'admin@jasa-kartini.com' }}</p>
                  </div>
                </div>
                
                <!-- Menu Links -->
                <div class="p-1">
                  <button @click="router.push('/admin/pengguna'); profileMenuOpen = false" 
                          class="w-full flex items-center gap-3 px-3 py-2 text-xs font-medium rounded hover:bg-surface-container-low text-on-surface transition-colors cursor-pointer text-left">
                    <span class="material-symbols-outlined text-sm text-secondary">group</span>
                    <span>Manajemen Pengguna</span>
                  </button>
                  <button @click="router.push('/admin/pengaturan'); profileMenuOpen = false" 
                          class="w-full flex items-center gap-3 px-3 py-2 text-xs font-medium rounded hover:bg-surface-container-low text-on-surface transition-colors cursor-pointer text-left">
                    <span class="material-symbols-outlined text-sm text-secondary">settings</span>
                    <span>Pengaturan Sistem</span>
                  </button>
                </div>
                
                <!-- Logout Divider -->
                <div class="border-t border-outline-variant/60 p-1 bg-surface-container-low">
                  <button @click="handleLogout" 
                          class="w-full flex items-center gap-3 px-3 py-2 text-xs font-bold rounded hover:bg-error-container hover:text-on-error-container text-error transition-all cursor-pointer text-left">
                    <span class="material-symbols-outlined text-sm">logout</span>
                    <span>Keluar (Logout)</span>
                  </button>
                </div>
              </div>
            </Transition>
          </div>
        </div>
      </header>

      <!-- Main Canvas -->
      <main class="p-container-padding flex-1 flex flex-col gap-section-gap">
        
        <!-- System Overview Metrics -->
        <section>
          <h2 class="font-headline-md text-headline-md text-primary mb-stack-md">Dashboard Overview</h2>
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-gutter">
            
            <!-- Metric Card 1: Total Penyakit -->
            <div class="bg-surface-container-lowest border border-outline-variant rounded p-stack-md flex flex-col gap-stack-sm hover:shadow-[0_4px_12px_rgba(26,54,93,0.05)] transition-shadow">
              <div class="flex justify-between items-center text-on-surface-variant">
                <span class="font-label-sm text-label-sm uppercase tracking-wider">Total Penyakit</span>
                <span class="material-symbols-outlined text-[20px]">medical_services</span>
              </div>
              <div class="font-headline-lg text-headline-lg text-primary">{{ stats.total_penyakit }}</div>
              <div class="font-body-sm text-body-sm text-secondary flex items-center gap-1">
                <span class="material-symbols-outlined text-[16px]">arrow_upward</span>
                +2 bulan ini
              </div>
            </div>

            <!-- Metric Card 2: Basis Aturan -->
            <div class="bg-surface-container-lowest border border-outline-variant rounded p-stack-md flex flex-col gap-stack-sm hover:shadow-[0_4px_12px_rgba(26,54,93,0.05)] transition-shadow">
              <div class="flex justify-between items-center text-on-surface-variant">
                <span class="font-label-sm text-label-sm uppercase tracking-wider">Basis Aturan</span>
                <span class="material-symbols-outlined text-[20px]">menu_book</span>
              </div>
              <div class="font-headline-lg text-headline-lg text-primary">{{ stats.total_aturan }}</div>
              <div class="font-body-sm text-body-sm text-secondary flex items-center gap-1">
                <span class="material-symbols-outlined text-[16px]">check_circle</span>
                Tersinkronisasi
              </div>
            </div>

            <!-- Metric Card 3: Total Gejala -->
            <div class="bg-surface-container-lowest border border-outline-variant rounded p-stack-md flex flex-col gap-stack-sm hover:shadow-[0_4px_12px_rgba(26,54,93,0.05)] transition-shadow">
              <div class="flex justify-between items-center text-on-surface-variant">
                <span class="font-label-sm text-label-sm uppercase tracking-wider">Total Gejala</span>
                <span class="material-symbols-outlined text-[20px]">stethoscope</span>
              </div>
              <div class="font-headline-lg text-headline-lg text-primary">{{ stats.total_gejala }}</div>
              <div class="font-body-sm text-body-sm text-on-surface-variant flex items-center gap-1">
                Menunggu validasi
              </div>
            </div>

            <!-- Metric Card 4: Pasien Terdiagnosa -->
            <div class="bg-surface-container-lowest border border-outline-variant rounded p-stack-md flex flex-col gap-stack-sm hover:shadow-[0_4px_12px_rgba(26,54,93,0.05)] transition-shadow">
              <div class="flex justify-between items-center text-on-surface-variant">
                <span class="font-label-sm text-label-sm uppercase tracking-wider">Pasien Terdiagnosa</span>
                <span class="material-symbols-outlined text-[20px]">group</span>
              </div>
              <div class="font-headline-lg text-headline-lg text-primary">{{ stats.total_riwayat }}</div>
              <div class="font-body-sm text-body-sm text-secondary flex items-center gap-1">
                <span class="material-symbols-outlined text-[16px]">trending_up</span>
                +12% vs pekan lalu
              </div>
            </div>

          </div>
        </section>

        <!-- Complex Layout Grid -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-gutter">
          
          <!-- Main Data Table Area (Spans 2 columns) -->
          <div class="lg:col-span-2 flex flex-col gap-gutter">
            <!-- Diagnosis History Table -->
            <section class="bg-surface-container-lowest border border-outline-variant rounded flex flex-col">
              <div class="p-stack-md border-b border-outline-variant flex justify-between items-center">
                <h3 class="font-headline-sm text-headline-sm text-primary">Riwayat Diagnosa Terkini</h3>
                <button @click="router.push('/admin/riwayat')" 
                        class="text-secondary font-label-md hover:bg-surface-container-low px-3 py-1 rounded transition-colors border border-transparent hover:border-secondary-container cursor-pointer">
                  Lihat Semua
                </button>
              </div>
              
              <div class="overflow-x-auto">
                <table class="w-full text-left border-collapse">
                  <thead>
                    <tr class="border-b border-primary bg-background">
                      <th class="p-stack-sm font-label-sm text-label-sm text-on-surface-variant uppercase tracking-wider pl-stack-md">Pasien</th>
                      <th class="p-stack-sm font-label-sm text-label-sm text-on-surface-variant uppercase tracking-wider">Diagnosa (THT)</th>
                      <th class="p-stack-sm font-label-sm text-label-sm text-on-surface-variant uppercase tracking-wider w-1/4">Probabilitas Bayes</th>
                      <th class="p-stack-sm font-label-sm text-label-sm text-on-surface-variant uppercase tracking-wider">Tanggal</th>
                      <th class="p-stack-sm font-label-sm text-label-sm text-on-surface-variant uppercase tracking-wider pr-stack-md text-right">Action</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-if="loading">
                      <td colspan="5" class="p-12 text-center text-on-surface-variant">
                        <div class="flex items-center justify-center gap-2">
                          <span class="w-4 h-4 border-2 border-t-transparent rounded-full animate-spin border-primary"></span>
                          <span>Memuat data riwayat...</span>
                        </div>
                      </td>
                    </tr>
                    <tr v-else-if="filteredDiagnoses.length === 0">
                      <td colspan="5" class="p-12 text-center text-on-surface-variant italic">Belum ada riwayat diagnosa</td>
                    </tr>
                    <tr v-else v-for="row in filteredDiagnoses" :key="row.id"
                        class="border-b border-outline-variant bg-surface-container-lowest hover:bg-surface-container-low transition-colors">
                      <td class="p-stack-sm pl-stack-md">
                        <div class="flex items-center gap-3">
                          <div class="w-8 h-8 rounded-full flex items-center justify-center font-bold text-xs shrink-0" :class="row.avatarCls">
                            {{ row.initials }}
                          </div>
                          <div>
                            <div class="font-body-md text-primary font-medium">{{ row.name }}</div>
                            <div class="font-label-sm text-on-surface-variant">Pasien Umum</div>
                          </div>
                        </div>
                      </td>
                      <td class="p-stack-sm font-body-sm text-on-surface">
                        <span class="inline-flex items-center px-2 py-1 rounded-full text-xs font-semibold border" :class="row.badgeCls">
                          {{ row.diagnosis }}
                        </span>
                      </td>
                      <td class="p-stack-sm font-body-sm text-on-surface">
                        <div class="flex items-center space-x-2">
                          <div class="flex-1 h-2 bg-surface-container-high rounded-full overflow-hidden">
                            <div class="h-full rounded-full transition-all duration-700" :class="row.barCls" :style="{width: row.probability}"></div>
                          </div>
                          <span class="font-semibold">{{ row.probability }}</span>
                        </div>
                      </td>
                      <td class="p-stack-sm font-body-sm text-on-surface">{{ row.date }}</td>
                      <td class="p-stack-sm pr-stack-md text-right">
                        <button @click="openDetails(row)"
                                class="text-on-surface-variant hover:text-primary p-1.5 rounded-md hover:bg-surface-container transition-colors cursor-pointer" title="View Details">
                          <span class="material-symbols-outlined text-[20px]">visibility</span>
                        </button>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </section>
          </div>

          <!-- Secondary Cards Area (Spans 1 column) -->
          <div class="flex flex-col gap-gutter">
            
            <!-- Knowledge Base Health -->
            <section class="bg-surface-container-lowest border border-outline-variant rounded p-stack-md flex flex-col gap-stack-md">
              <div class="flex justify-between items-start">
                <h3 class="font-headline-sm text-headline-sm text-primary">Aturan Klinis</h3>
                <span class="material-symbols-outlined text-secondary">verified_user</span>
              </div>
              <div class="flex flex-col gap-unit">
                <div class="flex justify-between items-center font-label-md text-on-surface-variant">
                  <span>Skor Validasi Aturan</span>
                  <span class="font-bold text-primary">{{ stats.validation_score || 0 }}%</span>
                </div>
                <div class="w-full bg-surface-container-high rounded-full h-2">
                  <div class="bg-secondary h-2 rounded-full transition-all duration-500" :style="{ width: (stats.validation_score || 0) + '%' }"></div>
                </div>
                <p class="font-body-sm text-body-sm text-on-surface-variant mt-2">
                  <span v-if="(stats.validation_score || 0) === 100">Seluruh penyakit sudah terpetakan dengan basis aturan yang lengkap.</span>
                  <span v-else-if="(stats.validation_score || 0) >= 70">Basis pengetahuan terpetakan dengan baik berdasarkan regulasi klinis THT.</span>
                  <span v-else>Basis pengetahuan memerlukan pembaruan aturan relasi penyakit.</span>
                </p>
              </div>
              <button @click="router.push('/admin/aturan')" 
                      class="bg-primary-container text-on-tertiary font-label-md py-2 px-4 rounded w-full flex items-center justify-center gap-2 hover:bg-primary transition-colors mt-auto cursor-pointer">
                <span class="material-symbols-outlined text-[18px]">update</span>
                Update Aturan
              </button>
            </section>

            <!-- Recent System Logs -->
            <section class="bg-surface-container-lowest border border-outline-variant rounded flex flex-col flex-1">
              <div class="p-stack-md border-b border-outline-variant">
                <h3 class="font-headline-sm text-headline-sm text-primary">Logs Sistem</h3>
              </div>
              <div class="flex flex-col p-stack-sm gap-unit">
                <div v-if="logs.length === 0" class="p-4 text-center text-on-surface-variant italic">
                  Belum ada log aktivitas sistem.
                </div>
                <div v-else v-for="(log, idx) in logs" :key="idx" 
                     class="p-2 flex items-start gap-3 hover:bg-surface-container-low rounded transition-colors">
                  <div class="p-1 rounded mt-1" :class="log.icon_cls">
                    <span class="material-symbols-outlined text-[16px]">{{ log.icon }}</span>
                  </div>
                  <div>
                    <div class="font-label-md text-primary">{{ log.title }}</div>
                    <div class="font-label-sm text-on-surface-variant leading-relaxed">{{ log.message }}</div>
                    <div class="font-label-sm text-outline mt-1">{{ log.time }}</div>
                  </div>
                </div>
              </div>
              <div class="p-stack-sm border-t border-outline-variant mt-auto">
                <a @click="router.push('/admin/riwayat')" class="font-label-md text-secondary text-center block w-full hover:underline cursor-pointer">View Audit Trail</a>
              </div>
            </section>

          </div>
        </div>
      </main>

      <!-- Footer -->
      <footer class="border-t border-outline-variant px-6 py-4 bg-surface-container-lowest">
        <p class="text-on-surface-variant text-xs text-center">© 2026 Sistem Pakar THT — Kelompok 2 · RS Jasa Kartini. All rights reserved.</p>
      </footer>
    </div>

    <!-- Details View Modal -->
    <Transition name="fade">
      <div v-if="detailModalOpen" class="fixed inset-0 z-50 flex items-center justify-center p-4">
        <!-- Overlay -->
        <div @click="detailModalOpen = false" class="absolute inset-0 bg-inverse-surface/60 backdrop-blur-sm"></div>
        <!-- Dialog -->
        <div class="relative w-full max-w-lg bg-surface-container-lowest rounded-xl shadow-2xl overflow-hidden border border-outline-variant">
          <div class="flex justify-between items-center px-6 py-4 border-b border-outline-variant bg-surface-container-low">
            <h3 class="font-bold text-primary flex items-center gap-2">
              <span class="material-symbols-outlined text-secondary">assignment</span>
              Detail Riwayat Diagnosa
            </h3>
            <button @click="detailModalOpen = false" class="text-on-surface-variant hover:text-on-surface cursor-pointer">
              <span class="material-symbols-outlined text-lg">close</span>
            </button>
          </div>
          <div class="p-6 space-y-4 text-sm" v-if="selectedRow">
            <div class="grid grid-cols-2 gap-4">
              <div>
                <p class="text-xs font-semibold text-on-surface-variant uppercase">Pasien</p>
                <p class="font-bold text-primary mt-1">{{ selectedRow.name }}</p>
              </div>
              <div>
                <p class="text-xs font-semibold text-on-surface-variant uppercase">Tanggal</p>
                <p class="font-bold text-primary mt-1">{{ selectedRow.date }}</p>
              </div>
            </div>
            <div>
              <p class="text-xs font-semibold text-on-surface-variant uppercase">Diagnosa Penyakit</p>
              <div class="mt-1 flex items-center gap-2">
                <span class="inline-flex items-center px-2 py-1 rounded-full text-xs font-semibold border"
                      :class="selectedRow.badgeCls">
                  {{ selectedRow.diagnosis }}
                </span>
                <span class="font-bold text-primary">{{ selectedRow.probability }}</span>
              </div>
            </div>
            <div>
              <p class="text-xs font-semibold text-on-surface-variant uppercase">Gejala Terdeteksi</p>
              <p class="font-medium text-on-surface-variant mt-1 leading-relaxed">{{ selectedRow.symptomsCount }} gejala dilaporkan.</p>
            </div>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth.store'
import { api } from '../../services/api.js'
import Sidebar from '../../components/Sidebar.vue'

const router = useRouter()
const authStore            = useAuthStore()
const sidebarOpen          = ref(false)
const loading              = ref(true)
const diagnoses            = ref([])
const stats                = ref({ total_penyakit: 0, total_gejala: 0, total_aturan: 0, total_riwayat: 0, validation_score: 0 })
const logs                 = ref([])
const searchQuery          = ref('')
const notificationMenuOpen = ref(false)
const profileMenuOpen      = ref(false)

const detailModalOpen = ref(false)
const selectedRow     = ref(null)

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}

const filteredDiagnoses = computed(() => {
  const q = searchQuery.value.trim().toLowerCase()
  if (!q) return diagnoses.value
  return diagnoses.value.filter(row => 
    (row.name && row.name.toLowerCase().includes(q)) ||
    (row.diagnosis && row.diagnosis.toLowerCase().includes(q))
  )
})

const getInitials = (name) => {
  if (!name) return '?'
  const parts = name.trim().split(/\s+/)
  return parts.length >= 2 ? (parts[0][0] + parts[1][0]).toUpperCase() : parts[0][0].toUpperCase()
}

// Avatar configurations matching the MedExpert clinical palette
const getAvatarCls = (index) => {
  const list = [
    'bg-secondary-container text-on-secondary-container',
    'bg-primary-fixed text-on-primary-fixed',
    'bg-tertiary-fixed text-on-tertiary-fixed',
    'bg-error-container text-on-error-container',
    'bg-surface-container-highest text-on-primary-fixed-variant'
  ]
  return list[index % list.length]
}

const getBadgeCls = (probability) => {
  const pct = parseInt(probability) || 0
  if (pct >= 85) {
    return 'bg-error-container text-on-error-container border-error/20'
  } else if (pct >= 70) {
    return 'bg-primary-container/10 text-on-primary-fixed-variant border-primary-container/20'
  }
  return 'bg-surface-container-highest text-on-surface-variant border-outline-variant/50'
}

const getBarCls = (probability) => {
  const pct = parseInt(probability) || 0
  if (pct >= 85) return 'bg-primary'
  if (pct >= 70) return 'bg-tertiary'
  return 'bg-secondary'
}

const formatDate = (dateString) => {
  if (!dateString) return '-'
  const dt = new Date(dateString)
  if (isNaN(dt.getTime())) return dateString
  return dt.toLocaleDateString('id-ID', { day: 'numeric', month: 'short', year: 'numeric' })
}

const fetchStats = async () => {
  loading.value = true
  try {
    const res = await api.getDashboardStats()
    if (res.success) {
      stats.value = res.stats
      logs.value = res.system_logs || []
      diagnoses.value = res.recent_diagnoses.map((item, index) => {
        const prob = Math.round(item.percentage) + '%'
        return {
          id: item.id,
          name: item.name,
          initials: getInitials(item.name),
          avatarCls: getAvatarCls(index),
          diagnosis: item.diagnosis,
          probability: prob,
          badgeCls: getBadgeCls(prob),
          barCls: getBarCls(prob),
          date: formatDate(item.tanggal),
          symptomsCount: item.symptoms_count
        }
      })
    }
  } catch (err) {
    console.error('Failed to load stats:', err)
  } finally {
    loading.value = false
  }
}

const openDetails = (row) => {
  selectedRow.value = row
  detailModalOpen.value = true
}

onMounted(fetchStats)
</script>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity 0.2s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>
