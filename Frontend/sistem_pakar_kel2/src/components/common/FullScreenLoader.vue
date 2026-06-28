<template>
  <Transition name="fade">
    <div v-if="isVisible" class="fixed inset-0 z-[9999] bg-surface/80 backdrop-blur-sm flex flex-col items-center justify-center">
      <div class="bg-surface-container-lowest border border-outline-variant p-6 rounded-2xl shadow-xl flex flex-col items-center max-w-xs text-center animate-in zoom-in duration-200">
        <div class="w-12 h-12 border-4 border-outline-variant border-t-primary rounded-full animate-spin mb-4"></div>
        <h3 class="font-headline-sm font-bold text-primary mb-1">{{ title }}</h3>
        <p class="font-body-sm text-on-surface-variant">{{ message }}</p>
      </div>
    </div>
  </Transition>
</template>

<script setup>
defineProps({
  isVisible: {
    type: Boolean,
    default: false
  },
  title: {
    type: String,
    default: 'Memuat'
  },
  message: {
    type: String,
    default: 'Harap tunggu sebentar...'
  }
})
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
