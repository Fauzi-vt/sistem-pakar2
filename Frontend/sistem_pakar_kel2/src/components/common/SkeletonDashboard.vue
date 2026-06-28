<template>
  <div class="animate-pulse">
    <!-- Breadcrumb & Header Skeleton -->
    <div class="h-4 bg-surface-container-high rounded w-32 mb-6"></div>
    <div class="h-8 bg-surface-container-high rounded w-64 mb-2"></div>
    <div class="h-4 bg-surface-container-high rounded w-96 mb-8"></div>

    <!-- Stats Skeleton -->
    <section class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
      <div v-for="i in 3" :key="i" class="bg-surface-container-lowest border border-outline-variant p-6 rounded-2xl flex items-center gap-4">
        <div class="w-12 h-12 rounded-full bg-surface-container-high shrink-0"></div>
        <div class="flex-1">
          <div class="h-3 bg-surface-container-high rounded w-24 mb-2"></div>
          <div class="h-6 bg-surface-container-high rounded w-16"></div>
        </div>
      </div>
    </section>

    <!-- Main Content Skeleton -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      
      <!-- Left Column -->
      <div class="lg:col-span-2 flex flex-col gap-6">
        <section class="bg-surface-container-lowest border border-outline-variant rounded-2xl p-6 h-40"></section>
        <section class="bg-surface-container-lowest border border-outline-variant rounded-2xl p-6 h-64"></section>
      </div>

      <!-- Right Column -->
      <div class="flex flex-col gap-6">
        <section class="bg-surface-container-lowest border border-outline-variant rounded-2xl p-6 h-40"></section>
        <section class="bg-surface-container-lowest border border-outline-variant rounded-2xl p-6 h-40"></section>
      </div>
    </div>
  </div>
</template>
