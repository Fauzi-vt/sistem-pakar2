<template>
  <div class="flex flex-col items-center justify-center p-12 bg-surface-container-lowest border border-outline-variant border-dashed rounded-xl text-center">
    <div class="w-20 h-20 mb-4 flex items-center justify-center bg-surface-container-low rounded-full">
      <component :is="IconComponent" class="w-10 h-10 text-on-surface-variant opacity-60" />
    </div>
    <h3 class="font-headline-sm text-headline-sm font-bold text-primary mb-2">{{ title }}</h3>
    <p class="font-body-md text-on-surface-variant max-w-md mb-6">{{ description }}</p>
    
    <button v-if="actionLabel" @click="$emit('action')" 
            class="bg-primary text-on-primary hover:bg-primary/90 px-6 py-2.5 rounded-lg font-label-md transition-colors shadow-sm cursor-pointer">
      {{ actionLabel }}
    </button>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import * as LucideIcons from 'lucide-vue-next'

const props = defineProps({
  icon: {
    type: String,
    default: 'FileSearch'
  },
  title: {
    type: String,
    required: true
  },
  description: {
    type: String,
    required: true
  },
  actionLabel: {
    type: String,
    default: ''
  }
})

defineEmits(['action'])

const IconComponent = computed(() => {
  return LucideIcons[props.icon] || LucideIcons.FileSearch
})
</script>
