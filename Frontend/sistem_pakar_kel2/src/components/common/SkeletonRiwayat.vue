<template>
  <div class="animate-pulse">
    <div class="bg-surface-container-lowest border border-outline-variant rounded-2xl p-6 mb-8">
      <!-- Toolbar Skeleton -->
      <div class="flex justify-between items-center mb-6">
        <div class="h-6 bg-surface-container-high rounded w-32"></div>
        <div class="h-10 bg-surface-container-high rounded w-64"></div>
      </div>
      
      <!-- Table Header Skeleton -->
      <div class="flex gap-4 border-b border-outline-variant pb-4 mb-4">
        <div class="h-4 bg-surface-container-high rounded w-1/4"></div>
        <div class="h-4 bg-surface-container-high rounded w-1/4"></div>
        <div class="h-4 bg-surface-container-high rounded w-1/4"></div>
        <div class="h-4 bg-surface-container-high rounded w-1/4"></div>
      </div>
      
      <!-- Table Rows Skeleton -->
      <div v-for="i in 5" :key="i" class="flex gap-4 py-4 border-b border-outline-variant/50">
        <div class="h-4 bg-surface-container-high rounded w-1/4"></div>
        <div class="h-4 bg-surface-container-high rounded w-1/4"></div>
        <div class="h-4 bg-surface-container-high rounded w-1/4"></div>
        <div class="h-4 bg-surface-container-high rounded w-1/4"></div>
      </div>
    </div>
  </div>
</template>
