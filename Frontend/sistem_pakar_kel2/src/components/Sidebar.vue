<template>
  <!-- Mobile Overlay -->
  <Transition name="fade">
    <div v-if="isOpen" @click="$emit('update:isOpen', false)"
      class="fixed inset-0 z-40 lg:hidden bg-on-surface/40 backdrop-blur-sm" />
  </Transition>

  <!-- Sidebar -->
  <aside
    class="bg-surface dark:bg-surface-container h-screen w-64 fixed left-0 top-0 flex flex-col p-stack-lg border-r border-outline-variant z-50
           -translate-x-full lg:translate-x-0 transition-transform duration-300 ease-in-out gap-stack-lg"
    :class="{ 'translate-x-0': isOpen }">

    <!-- Header Info / Brand logo -->
    <div class="flex items-center gap-stack-sm relative shrink-0">
      <img alt="System Logo" class="w-8 h-8 rounded" src="https://lh3.googleusercontent.com/aida-public/AB6AXuCAJXOgjy8Ss4jxCEKmfuSn3ckjvlyJoiIRl_NpqhWfJkOoleTXZnsJR_HabCKCvcTgpJ7J30MjCMuVq02KnE6bLd0V4M-2eR36KmfvuW8lSel-nU__NYMpVDp-hQXJ2hT4mNvkYoNlYbUKomtsFdV7my-BLT1s_FzJXAgC0v1F5_ehSbsLbYSfe8sW_uxvIobye2BaFIL1_ZZKd2kqr2uShj1RVb2DoTsqImaTVaoJlsTMs_oMR0bn-VXhUdD0Du7M1Hu6wcVC42Sj">
      <div>
        <h1 class="font-headline-sm text-headline-sm font-black text-primary leading-tight">MedExpert</h1>
        <p class="font-label-sm text-label-sm text-on-surface-variant">Admin Panel</p>
      </div>

      <!-- Mobile Close Button -->
      <button @click="$emit('update:isOpen', false)"
        class="absolute right-0 top-1/2 -translate-y-1/2 lg:hidden w-8 h-8 rounded-lg flex items-center justify-center text-outline hover:bg-surface-container hover:text-on-surface transition-colors">
        <span class="material-symbols-outlined text-lg">close</span>
      </button>
    </div>

    <!-- Quick Action / New Assessment Button -->
    <!-- Quick Action / New Assessment Button -->
    <button @click="startNewAssessment"
      class="bg-primary-container text-on-tertiary font-label-md py-2 px-4 rounded w-full flex items-center justify-center gap-2 hover:bg-primary transition-colors cursor-pointer shrink-0">
      <span class="material-symbols-outlined text-[18px]">add</span>
      Asesmen Baru
    </button>
 
    <!-- Navigation Links -->
    <ul class="flex flex-col gap-unit flex-1 overflow-y-auto">
      <li v-for="item in navLinks" :key="item.label" class="cursor-pointer group">
        <!-- If item has a real route in our router -->
        <router-link v-if="item.to" :to="item.to" @click="$emit('update:isOpen', false)" custom v-slot="{ isActive, navigate }">
          <button @click="navigate"
            class="flex items-center gap-stack-sm p-2 w-full rounded-lg transition-all scale-98 active:scale-95 text-left cursor-pointer"
            :class="isActive 
              ? 'text-primary font-bold bg-secondary-container' 
              : 'text-on-surface-variant font-medium hover:bg-surface-container'"
          >
            <span class="material-symbols-outlined transition-colors"
                  :style="isActive ? 'font-variation-settings: \'FILL\' 1;' : ''">
              {{ item.icon }}
            </span>
            <span class="font-label-md text-label-md">{{ item.label }}</span>
          </button>
        </router-link>

        <!-- Static placeholder menu items matching the design layout -->
        <button v-else
          class="flex items-center gap-stack-sm p-2 w-full rounded-lg transition-all scale-98 active:scale-95 text-left text-on-surface-variant font-medium hover:bg-surface-container cursor-pointer"
        >
          <span class="material-symbols-outlined transition-colors">
            {{ item.icon }}
          </span>
          <span class="font-label-md text-label-md">{{ item.label }}</span>
        </button>
      </li>
    </ul>

    <!-- Footer Tab / Logout -->
    <div class="pt-4 border-t border-outline-variant shrink-0">
      <button @click="handleLogout"
        class="w-full flex items-center gap-stack-sm p-2 rounded-lg font-bold text-error hover:bg-error-container/30 active:scale-95 transition-all text-left cursor-pointer">
        <span class="material-symbols-outlined">logout</span>
        <span class="font-label-md text-label-md">Keluar</span>
      </button>
    </div>
  </aside>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth.store'

defineProps({ isOpen: { type: Boolean, default: false } })
defineEmits(['update:isOpen'])

const router = useRouter()
const authStore = useAuthStore()
const handleLogout = () => { authStore.logout(); router.push('/login') }

const startNewAssessment = () => {
  router.push('/diagnosa')
}

// Map real system routes directly to corresponding menu keys
const navLinks = [
  { to: '/admin/dashboard',   label: 'Dashboard',             icon: 'dashboard' },
  { to: '/admin/penyakit',    label: 'Data Penyakit',         icon: 'medical_services' },
  { to: '/admin/gejala',      label: 'Data Gejala',           icon: 'stethoscope' },
  { to: '/admin/riwayat',     label: 'Riwayat Diagnosa',      icon: 'history' },
  { to: '/admin/aturan',      label: 'Basis Aturan',          icon: 'menu_book' },
  { to: '/admin/pengguna',    label: 'Manajemen Pengguna',    icon: 'group' },
  { to: '/admin/kesehatan',   label: 'Status Sistem',         icon: 'monitor_heart' },
  { to: '/admin/statistik',   label: 'Statistik Diagnosa',    icon: 'query_stats' },
  { to: '/admin/pengaturan',  label: 'Pengaturan Sistem',     icon: 'settings' },
]
</script>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity 0.25s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>
