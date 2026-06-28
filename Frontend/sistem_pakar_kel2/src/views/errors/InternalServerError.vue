<template>
  <div class="min-h-screen flex items-center justify-center bg-surface p-4">
    <div class="max-w-md text-center">
      <div class="w-32 h-32 mx-auto mb-8 bg-error-container text-error rounded-full flex items-center justify-center">
        <span class="material-symbols-outlined text-6xl">dns</span>
      </div>
      <h1 class="text-6xl font-black text-primary mb-4 tracking-tight">500</h1>
      <h2 class="text-2xl font-bold text-on-surface mb-2">Kesalahan Server Internal</h2>
      <p class="text-on-surface-variant font-body-md mb-8">
        Terjadi masalah pada server kami saat mencoba memproses permintaan Anda. Tim kami telah diberitahu. Silakan coba lagi beberapa saat.
      </p>
      <div class="flex gap-4 justify-center">
        <button @click="goBack"
                class="bg-surface-container border border-outline hover:border-primary text-on-surface px-6 py-3 rounded-lg font-bold flex items-center gap-2 transition-colors cursor-pointer">
          <span class="material-symbols-outlined text-[20px]">arrow_back</span>
          Kembali
        </button>
        <button @click="refreshPage"
                class="bg-primary hover:bg-primary/90 text-on-primary px-6 py-3 rounded-lg font-bold flex items-center gap-2 transition-colors shadow-sm cursor-pointer">
          <span class="material-symbols-outlined text-[20px]">refresh</span>
          Muat Ulang
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const goBack = () => {
  router.go(-2) // Go back 2 steps assuming step 1 is the bad API page and this is an overlay, or just -1
}

const refreshPage = () => {
  window.location.reload()
}
</script>
