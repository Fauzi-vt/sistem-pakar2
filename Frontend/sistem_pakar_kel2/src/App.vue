<template>
  <div class="min-h-screen bg-slate-50 text-slate-800 antialiased font-sans flex flex-col">
    <router-view />
    <Toast />
    <ConfirmDialog />
  </div>
</template>

<script setup>
import { onMounted, onUnmounted } from 'vue'
import { useToast } from 'primevue/usetoast'
import Toast from 'primevue/toast'
import ConfirmDialog from 'primevue/confirmdialog'

const toast = useToast()

const handleGlobalError = (e) => {
  toast.add({ severity: 'error', summary: 'Network Error', detail: e.detail, life: 5000 })
}

onMounted(() => {
  window.addEventListener('global-error', handleGlobalError)
})

onUnmounted(() => {
  window.removeEventListener('global-error', handleGlobalError)
})
</script>

<style>
/* Global smooth styles */
html, body {
  margin: 0;
  padding: 0;
  font-family: 'Inter', sans-serif;
}
</style>
