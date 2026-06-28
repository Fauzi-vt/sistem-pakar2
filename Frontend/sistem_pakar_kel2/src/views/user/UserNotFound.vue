<template>
  <UserLayout>
    <div class="min-h-[70vh] flex flex-col items-center justify-center text-center">
      <div class="w-24 h-24 bg-surface-container-low rounded-full flex items-center justify-center mb-6">
        <span class="material-symbols-outlined text-[48px] text-on-surface-variant opacity-60">route</span>
      </div>
      <h1 class="text-3xl font-bold text-primary mb-2">Halaman Tidak Ditemukan</h1>
      <p class="text-on-surface-variant max-w-md mb-8">Maaf, halaman yang Anda tuju tidak tersedia atau telah dipindahkan.</p>
      
      <button @click="$router.push('/user/dashboard')" 
              class="bg-primary text-on-primary hover:bg-primary/90 px-6 py-3 rounded-lg font-bold flex items-center gap-2 transition-all cursor-pointer">
        <span class="material-symbols-outlined text-[20px]">home</span>
        Kembali ke Dashboard
      </button>
    </div>
  </UserLayout>
</template>

<script setup>
import UserLayout from '@/layouts/UserLayout.vue'
</script>
