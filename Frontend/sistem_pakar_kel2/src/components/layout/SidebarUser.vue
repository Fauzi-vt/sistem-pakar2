<template>
  <!-- Mobile Overlay -->
  <Transition name="fade">
    <div v-if="isOpen" @click="$emit('update:isOpen', false)"
      class="fixed inset-0 z-40 lg:hidden bg-on-surface/40 backdrop-blur-sm" />
  </Transition>

  <!-- Sidebar -->
  <aside
    class="bg-surface dark:bg-surface-container h-screen w-64 fixed left-0 top-0 flex flex-col p-stack-lg border-r border-outline-variant z-50
           -translate-x-full lg:translate-x-0 transition-transform duration-300 ease-in-out"
    :class="{ 'translate-x-0': isOpen }">

    <!-- User Identity Header -->
    <div class="flex items-center gap-stack-sm mb-6 bg-surface-container-low p-3 rounded-xl border border-outline-variant/50 shrink-0">
      <div class="w-10 h-10 rounded-full bg-primary-container text-on-primary-container flex items-center justify-center font-bold text-lg shrink-0">
        {{ userInitial }}
      </div>
      <div class="flex-1 min-w-0">
        <h2 class="font-headline-sm text-[15px] font-bold text-primary truncate leading-tight">{{ userName }}</h2>
        <p class="font-label-sm text-xs text-on-surface-variant capitalize">{{ userRole }}</p>
      </div>

      <!-- Mobile Close Button -->
      <button @click="$emit('update:isOpen', false)"
        class="lg:hidden w-8 h-8 rounded flex items-center justify-center text-outline hover:bg-surface-container hover:text-on-surface transition-colors shrink-0">
        <span class="material-symbols-outlined text-lg">close</span>
      </button>
    </div>

    <!-- Navigation Links -->
    <div class="flex flex-col flex-1 overflow-y-auto gap-4">
      
      <!-- Primary Actions Group -->
      <ul class="flex flex-col gap-1">
        <li v-for="item in primaryLinks" :key="item.label">
          <router-link :to="item.to" @click="$emit('update:isOpen', false)" custom v-slot="{ isActive, navigate }">
            <button @click="navigate"
              class="flex items-center gap-stack-sm p-2.5 w-full rounded-lg transition-all scale-98 active:scale-95 text-left cursor-pointer"
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
        </li>
      </ul>

      <!-- Divider -->
      <div class="h-px bg-outline-variant/40 mx-2"></div>

      <!-- Secondary Info Group -->
      <ul class="flex flex-col gap-1">
        <li v-for="item in secondaryLinks" :key="item.label">
          <router-link :to="item.to" @click="$emit('update:isOpen', false)" custom v-slot="{ isActive, navigate }">
            <button @click="navigate"
              class="flex items-center gap-stack-sm p-2.5 w-full rounded-lg transition-all scale-98 active:scale-95 text-left cursor-pointer"
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
        </li>
      </ul>

    </div>

    <!-- Footer Logout -->
    <div class="pt-4 border-t border-outline-variant shrink-0 mt-auto">
      <button @click="handleLogout"
        class="w-full flex items-center gap-stack-sm p-2.5 rounded-lg font-bold text-error hover:bg-error-container/30 active:scale-95 transition-all text-left cursor-pointer">
        <span class="material-symbols-outlined">logout</span>
        <span class="font-label-md text-label-md">Keluar</span>
      </button>
      <div class="mt-4 flex justify-center">
        <ThemeSwitch />
      </div>
    </div>
  </aside>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth.store'
import ThemeSwitch from '@/components/common/ThemeSwitch.vue'

defineProps({ isOpen: { type: Boolean, default: false } })
defineEmits(['update:isOpen'])

const router = useRouter()
const authStore = useAuthStore()

const userName = computed(() => authStore.currentUser?.name || 'Pasien THT')
const userRole = computed(() => authStore.currentUser?.role || 'user')
const userInitial = computed(() => {
  if (authStore.currentUser?.name) {
    return authStore.currentUser.name.charAt(0).toUpperCase()
  }
  return 'U'
})

const handleLogout = () => { 
  authStore.logout()
  router.push('/login') 
}

// Menu groupings matching professional dashboard style
const primaryLinks = [
  { to: '/user/dashboard', label: 'Dashboard', icon: 'home' },
  { to: '/user/diagnosa',  label: 'Konsultasi', icon: 'stethoscope' },
  { to: '/user/riwayat',   label: 'Riwayat Diagnosa', icon: 'history' }
]

const secondaryLinks = [
  { to: '/user/edukasi',   label: 'Tentang Sistem', icon: 'info' },
  { to: '/user/profil',    label: 'Profil Akun', icon: 'person' }
]
</script>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity 0.25s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>
