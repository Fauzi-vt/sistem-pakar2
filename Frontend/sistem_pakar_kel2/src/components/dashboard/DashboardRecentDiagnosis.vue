<template>
  <section class="bg-surface-container-lowest border border-outline-variant rounded flex flex-col">
    <div class="p-stack-md border-b border-outline-variant flex justify-between items-center">
      <h3 class="font-headline-sm text-headline-sm text-primary">Riwayat Diagnosa Terkini</h3>
      <button @click="$emit('view-all')" 
              class="text-secondary font-label-md hover:bg-surface-container-low px-3 py-1 rounded transition-colors border border-transparent hover:border-secondary-container cursor-pointer">
        Lihat Semua
      </button>
    </div>
    
    <div class="overflow-x-auto">
      <table class="w-full text-left border-collapse">
        <thead>
          <tr class="border-b border-primary bg-background">
            <th class="p-stack-sm font-label-sm text-label-sm text-on-surface-variant uppercase tracking-wider pl-stack-md">Pasien</th>
            <th class="p-stack-sm font-label-sm text-label-sm text-on-surface-variant uppercase tracking-wider">Diagnosa (THT)</th>
            <th class="p-stack-sm font-label-sm text-label-sm text-on-surface-variant uppercase tracking-wider w-1/4">Probabilitas Bayes</th>
            <th class="p-stack-sm font-label-sm text-label-sm text-on-surface-variant uppercase tracking-wider">Tanggal</th>
            <th class="p-stack-sm font-label-sm text-label-sm text-on-surface-variant uppercase tracking-wider pr-stack-md text-right">Aksi</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="loading">
            <td colspan="5" class="p-12 text-center text-on-surface-variant">
              <div class="flex items-center justify-center gap-2">
                <span class="w-4 h-4 border-2 border-t-transparent rounded-full animate-spin border-primary"></span>
                <span>Memuat data riwayat...</span>
              </div>
            </td>
          </tr>
          <tr v-else-if="diagnoses.length === 0">
            <td colspan="5" class="p-12 text-center text-on-surface-variant italic">Belum ada riwayat diagnosa</td>
          </tr>
          <tr v-else v-for="row in diagnoses" :key="row.id"
              class="border-b border-outline-variant bg-surface-container-lowest hover:bg-surface-container-low transition-colors">
            <td class="p-stack-sm pl-stack-md">
              <div class="flex items-center gap-3">
                <div class="w-8 h-8 rounded-full flex items-center justify-center font-bold text-xs shrink-0" :class="row.avatarCls">
                  {{ row.initials }}
                </div>
                <div>
                  <div class="font-body-md text-primary font-medium">{{ row.name }}</div>
                  <div class="font-label-sm text-on-surface-variant">Pasien Umum</div>
                </div>
              </div>
            </td>
            <td class="p-stack-sm font-body-sm text-on-surface">
              <span class="inline-flex items-center px-2 py-1 rounded-full text-xs font-semibold border" :class="row.badgeCls">
                {{ row.diagnosis }}
              </span>
            </td>
            <td class="p-stack-sm font-body-sm text-on-surface">
              <div class="flex items-center space-x-2">
                <div class="flex-1 h-2 bg-surface-container-high rounded-full overflow-hidden">
                  <div class="h-full rounded-full transition-all duration-700" :class="row.barCls" :style="{width: row.probability}"></div>
                </div>
                <span class="font-semibold">{{ row.probability }}</span>
              </div>
            </td>
            <td class="p-stack-sm font-body-sm text-on-surface">{{ row.date }}</td>
            <td class="p-stack-sm pr-stack-md text-right">
              <button @click="openDetails(row)"
                      class="text-on-surface-variant hover:text-primary p-1.5 rounded-md hover:bg-surface-container transition-colors cursor-pointer" title="Detail Diagnosa">
                <Eye class="w-5 h-5" />
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Detail Modal -->
    <Transition name="fade">
      <div v-if="detailModalOpen && selectedRow" 
           class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-on-surface/40 backdrop-blur-sm">
        <div class="bg-surface-container-lowest border border-outline-variant rounded-lg w-full max-w-lg shadow-2xl overflow-hidden flex flex-col">
          <div class="p-stack-md border-b border-outline-variant flex justify-between items-center bg-surface-container-low">
            <h3 class="font-headline-sm text-headline-sm text-primary flex items-center gap-2">
              <ShieldAlert class="w-5 h-5 text-secondary" />
              <span>Detail Diagnosa THT</span>
            </h3>
            <button @click="detailModalOpen = false" class="text-on-surface-variant hover:bg-surface-container rounded p-1 cursor-pointer">
              <X class="w-5 h-5" />
            </button>
          </div>
          <div class="p-stack-lg flex flex-col gap-stack-md overflow-y-auto max-h-[70vh] text-left">
            <div class="flex items-center gap-4 p-stack-md bg-surface-container rounded border border-outline-variant/50">
              <div class="w-12 h-12 rounded-full flex items-center justify-center font-bold text-lg" :class="selectedRow.avatarCls">
                {{ selectedRow.initials }}
              </div>
              <div>
                <p class="font-bold text-primary text-base">{{ selectedRow.name }}</p>
                <p class="text-xs text-on-surface-variant mt-0.5">Tanggal Periksa: {{ selectedRow.date }}</p>
              </div>
            </div>
            <div class="grid grid-cols-2 gap-gutter border-b border-outline-variant pb-stack-md">
              <div>
                <p class="text-xs font-semibold text-on-surface-variant uppercase">Hasil Diagnosa</p>
                <p class="font-bold text-primary text-lg mt-1">{{ selectedRow.diagnosis }}</p>
              </div>
              <div>
                <p class="text-xs font-semibold text-on-surface-variant uppercase">Probabilitas Bayes</p>
                <p class="font-bold text-secondary text-lg mt-1">{{ selectedRow.probability }}</p>
              </div>
            </div>
            <div>
              <p class="text-xs font-semibold text-on-surface-variant uppercase">Gejala Terdeteksi</p>
              <p class="font-medium text-on-surface-variant mt-1 leading-relaxed">{{ selectedRow.symptomsCount }} gejala dilaporkan.</p>
            </div>
          </div>
        </div>
      </div>
    </Transition>
  </section>
</template>

<script setup>
import { ref } from 'vue'
import { Eye, X, ShieldAlert } from 'lucide-vue-next'

defineProps({
  diagnoses: {
    type: Array,
    required: true,
    default: () => []
  },
  loading: {
    type: Boolean,
    default: false
  }
})

defineEmits(['view-all'])

const detailModalOpen = ref(false)
const selectedRow = ref(null)

const openDetails = (row) => {
  selectedRow.value = row
  detailModalOpen.value = true
}
</script>
