<template>
  <div class="min-h-screen bg-background text-on-background font-body-md flex relative antialiased">
    <!-- Sidebar -->
    <SidebarUser v-model:isOpen="sidebarOpen" />

    <!-- Main Content Wrapper -->
    <div class="flex-1 flex flex-col min-h-screen lg:ml-64 transition-all duration-300">
      
      <!-- Top Mobile Navbar (hanya muncul di mobile) -->
      <header class="lg:hidden bg-surface-container-lowest border-b border-outline-variant flex items-center justify-between h-16 px-4 sticky top-0 z-30">
        <div class="font-headline-sm text-[16px] font-bold text-primary">MedExpert</div>
        <button @click="sidebarOpen = true" class="p-2 rounded-lg hover:bg-surface-container transition-colors text-on-surface">
          <span class="material-symbols-outlined">menu</span>
        </button>
      </header>

      <!-- Page Content -->
      <main class="flex-1 p-4 md:p-6 lg:p-8 max-w-7xl mx-auto w-full">
        <slot></slot>
      </main>

    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import SidebarUser from '@/components/layout/SidebarUser.vue'

const sidebarOpen = ref(false)
</script>
