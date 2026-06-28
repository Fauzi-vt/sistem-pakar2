<template>
  <div class="flex flex-col items-center justify-center p-12 bg-error-container/20 border border-error/30 rounded-2xl text-center">
    <div class="w-16 h-16 rounded-full bg-error-container text-error flex items-center justify-center mb-4">
      <span class="material-symbols-outlined text-3xl">warning</span>
    </div>
    <h3 class="font-headline-sm font-bold text-error mb-2">Terjadi Kesalahan</h3>
    <p class="font-body-sm text-on-surface-variant max-w-sm mb-6">
      Komponen ini gagal dimuat. Silakan coba muat ulang bagian ini.
    </p>
    <button @click="$emit('retry')"
            class="bg-error hover:bg-error/90 text-white px-5 py-2.5 rounded-lg font-label-md transition-colors flex items-center gap-2 cursor-pointer shadow-sm">
      <span class="material-symbols-outlined text-[18px]">refresh</span>
      Coba Lagi
    </button>
  </div>
</template>

<script setup>
defineEmits(['retry'])
</script>
