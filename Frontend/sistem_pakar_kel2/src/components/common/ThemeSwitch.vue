<template>
  <button @click="toggleTheme" 
          class="w-10 h-10 rounded-full flex items-center justify-center transition-colors cursor-pointer"
          :class="isDark ? 'bg-surface-container-high text-primary hover:bg-surface-container-highest' : 'bg-surface-container-low text-on-surface hover:bg-surface-container-high'"
          :title="isDark ? 'Ganti ke Terang' : 'Ganti ke Gelap'"
          aria-label="Toggle Dark Mode">
    <span class="material-symbols-outlined text-[20px]">{{ isDark ? 'light_mode' : 'dark_mode' }}</span>
  </button>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const isDark = ref(false)

const toggleTheme = () => {
  isDark.value = !isDark.value
  const html = document.documentElement
  if (isDark.value) {
    html.classList.add('dark')
    localStorage.setItem('theme', 'dark')
  } else {
    html.classList.remove('dark')
    localStorage.setItem('theme', 'light')
  }
}

onMounted(() => {
  const savedTheme = localStorage.getItem('theme')
  if (savedTheme) {
    isDark.value = savedTheme === 'dark'
  } else {
    // Check system preference
    isDark.value = window.matchMedia('(prefers-color-scheme: dark)').matches
  }

  if (isDark.value) {
    document.documentElement.classList.add('dark')
  } else {
    document.documentElement.classList.remove('dark')
  }
})
</script>
