<template>
  <div class="min-h-screen flex items-center justify-center bg-surface p-4">
    <div class="max-w-md text-center">
      <div class="w-32 h-32 mx-auto mb-8 bg-error-container text-error rounded-full flex items-center justify-center animate-bounce">
        <span class="material-symbols-outlined text-6xl">gpp_bad</span>
      </div>
      <h1 class="text-6xl font-black text-primary mb-4 tracking-tight">403</h1>
      <h2 class="text-2xl font-bold text-on-surface mb-2">Akses Ditolak</h2>
      <p class="text-on-surface-variant font-body-md mb-8">
        Maaf, Anda tidak memiliki izin (Forbidden) untuk mengakses halaman ini. Halaman ini mungkin khusus untuk peran lain.
      </p>
      <button @click="goBack"
              class="bg-primary hover:bg-primary/90 text-on-primary px-6 py-3 rounded-lg font-bold flex items-center gap-2 mx-auto transition-colors shadow-sm cursor-pointer">
        <span class="material-symbols-outlined text-[20px]">arrow_back</span>
        Kembali ke Beranda
      </button>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth.store'

const router = useRouter()
const authStore = useAuthStore()

const goBack = () => {
  if (authStore.isAdmin) {
    router.push('/admin/dashboard')
  } else {
    router.push('/user/dashboard')
  }
}
</script>
