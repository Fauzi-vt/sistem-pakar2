<template>
  <div class="min-h-screen bg-slate-50 text-slate-800 antialiased font-sans flex flex-col">
    <router-view />
    <Toast />
    <ConfirmDialog />
  </div>
</template>

<script setup>
import Toast from 'primevue/toast'
import ConfirmDialog from 'primevue/confirmdialog'
</script>

<style>
/* Global smooth styles */
html, body {
  margin: 0;
  padding: 0;
  font-family: 'Inter', sans-serif;
}
</style>
