<template>
  <nav aria-label="Breadcrumb" class="mb-4">
    <ol class="flex items-center gap-2 font-body-sm text-on-surface-variant">
      <li v-for="(item, index) in items" :key="index" class="flex items-center gap-2">
        <router-link v-if="item.to" :to="item.to" class="hover:text-primary transition-colors cursor-pointer">
          {{ item.label }}
        </router-link>
        <span v-else class="text-on-surface font-medium">{{ item.label }}</span>
        
        <span v-if="index < items.length - 1" class="material-symbols-outlined text-[16px] opacity-50">
          chevron_right
        </span>
      </li>
    </ol>
  </nav>
</template>

<script setup>
defineProps({
  items: {
    type: Array,
    required: true,
    // Example: [{ label: 'Dashboard', to: '/user/dashboard' }, { label: 'Riwayat' }]
  }
})
</script>
