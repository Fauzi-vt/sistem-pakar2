<template>
  <header class="mb-stack-lg">
    <h1 class="font-headline-md text-headline-md font-bold text-primary mb-1">{{ title }}</h1>
    <p v-if="description" class="font-body-md text-on-surface-variant">{{ description }}</p>
  </header>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    required: true
  },
  description: {
    type: String,
    default: ''
  }
})
</script>
