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
            <Menu class="w-5 h-5 text-on-surface" />
          </button>
          <div class="relative w-full hidden sm:block">
            <Search class="absolute left-3 top-1/2 -translate-y-1/2 text-on-surface-variant w-5 h-5" />
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
              <Bell class="w-5 h-5" />
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
            <Settings class="w-5 h-5" />
          </button>

          <!-- Theme Switch -->
          <ThemeSwitch />

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
                    <Users class="text-secondary w-4 h-4 mr-1 shrink-0" />
                    <span>Manajemen Pengguna</span>
                  </button>
                  <button @click="router.push('/admin/pengaturan'); profileMenuOpen = false" 
                          class="w-full flex items-center gap-3 px-3 py-2 text-xs font-medium rounded hover:bg-surface-container-low text-on-surface transition-colors cursor-pointer text-left">
                    <Settings class="text-secondary w-4 h-4 mr-1 shrink-0" />
                    <span>Pengaturan Sistem</span>
                  </button>
                </div>
                
                <!-- Logout Divider -->
                <div class="border-t border-outline-variant/60 p-1 bg-surface-container-low">
                  <button @click="handleLogout" 
                          class="w-full flex items-center gap-3 px-3 py-2 text-xs font-bold rounded hover:bg-error-container hover:text-on-error-container text-error transition-all cursor-pointer text-left">
                    <LogOut class="w-4 h-4 mr-1 shrink-0" />
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
        <DashboardSummary :stats="stats" />
        
        <!-- Complex Layout Grid -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-gutter">
          <!-- Main Data Table Area (Spans 2 columns) -->
          <div class="lg:col-span-2 flex flex-col gap-gutter">
            <DashboardRecentDiagnosis 
              :diagnoses="filteredDiagnoses" 
              :loading="loading" 
              @view-all="router.push('/admin/riwayat')" 
            />
          </div>
          
          <!-- Secondary Cards Area (Spans 1 column) -->
          <DashboardChart 
            :stats="stats" 
            :logs="logs" 
            @update-rules="router.push('/admin/aturan')" 
            @view-audit="router.push('/admin/riwayat')" 
          />
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth.store'
import { api } from '../../services/api.js'
import Sidebar from '../../components/Sidebar.vue'
import DashboardSummary from '@/components/dashboard/DashboardSummary.vue'
import DashboardRecentDiagnosis from '@/components/dashboard/DashboardRecentDiagnosis.vue'
import DashboardChart from '@/components/dashboard/DashboardChart.vue'
import ThemeSwitch from '@/components/common/ThemeSwitch.vue'
import { Menu, Search, Bell, Settings, Users, LogOut } from 'lucide-vue-next'

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
onMounted(fetchStats)
</script>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity 0.2s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>
