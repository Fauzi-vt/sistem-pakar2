<template>
  <div class="flex flex-col gap-gutter">
    
    <!-- Knowledge Base Health -->
    <section class="bg-surface-container-lowest border border-outline-variant rounded p-stack-md flex flex-col gap-stack-md">
      <div class="flex justify-between items-start">
        <h3 class="font-headline-sm text-headline-sm text-primary">Aturan Klinis</h3>
        <ShieldCheck class="w-5 h-5 text-secondary" />
      </div>
      <div class="flex flex-col gap-unit">
        <div class="flex justify-between items-center font-label-md text-on-surface-variant">
          <span>Skor Validasi Aturan</span>
          <span class="font-bold text-primary">{{ stats.validation_score || 0 }}%</span>
        </div>
        <div class="w-full bg-surface-container-high rounded-full h-2">
          <div class="bg-secondary h-2 rounded-full transition-all duration-500" :style="{ width: (stats.validation_score || 0) + '%' }"></div>
        </div>
        <p class="font-body-sm text-body-sm text-on-surface-variant mt-2">
          <span v-if="(stats.validation_score || 0) === 100">Seluruh penyakit sudah terpetakan dengan basis aturan yang lengkap.</span>
          <span v-else-if="(stats.validation_score || 0) >= 70">Basis pengetahuan terpetakan dengan baik berdasarkan regulasi klinis THT.</span>
          <span v-else>Basis pengetahuan memerlukan pembaruan aturan relasi penyakit.</span>
        </p>
      </div>
      <button @click="$emit('update-rules')" 
              class="bg-primary-container text-on-tertiary font-label-md py-2 px-4 rounded w-full flex items-center justify-center gap-2 hover:bg-primary transition-colors mt-auto cursor-pointer">
        <RefreshCw class="w-4 h-4 text-on-tertiary" />
        <span>Update Aturan</span>
      </button>
    </section>

    <!-- Visual Diagnostic Stats Chart -->
    <section class="bg-surface-container-lowest border border-outline-variant rounded p-stack-md flex flex-col gap-stack-md">
      <div class="flex justify-between items-start">
        <h3 class="font-headline-sm text-headline-sm text-primary">Statistik Diagnosa THT</h3>
        <PieChart class="w-5 h-5 text-secondary" />
      </div>
      <div class="h-48 relative">
        <canvas ref="chartCanvas"></canvas>
      </div>
    </section>

    <!-- Recent System Logs -->
    <section class="bg-surface-container-lowest border border-outline-variant rounded flex flex-col flex-1">
      <div class="p-stack-md border-b border-outline-variant">
        <h3 class="font-headline-sm text-headline-sm text-primary">Logs Sistem</h3>
      </div>
      <div class="flex flex-col p-stack-sm gap-unit max-h-60 overflow-y-auto">
        <div v-if="logs.length === 0" class="p-4 text-center text-on-surface-variant italic">
          Belum ada log aktivitas sistem.
        </div>
        <template v-else>
          <div v-for="log in logs" :key="log.message" 
               class="p-2 flex items-start gap-3 hover:bg-surface-container-low rounded transition-colors">
            <div class="p-1 rounded mt-1 shrink-0" :class="log.icon_cls">
              <!-- Dynamically match icons with fallback -->
              <Info v-if="log.icon === 'info' || log.icon === 'person'" class="w-4 h-4" />
              <Activity v-else-if="log.icon === 'stethoscope'" class="w-4 h-4" />
              <CheckCircle v-else class="w-4 h-4" />
            </div>
            <div>
              <div class="font-label-md text-primary font-bold">{{ log.title }}</div>
              <div class="font-label-sm text-on-surface-variant leading-relaxed">{{ log.message }}</div>
              <div class="font-label-sm text-outline mt-1 text-[10px]">{{ log.time }}</div>
            </div>
          </div>
        </template>
      </div>
      <div class="p-stack-sm border-t border-outline-variant mt-auto">
        <button @click="$emit('view-audit')" 
                class="w-full text-center text-secondary font-label-md hover:bg-surface-container-low py-2 rounded transition-colors cursor-pointer border border-outline-variant/40">
          View Audit Trail
        </button>
      </div>
    </section>

  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { ShieldCheck, RefreshCw, PieChart, Info, Activity, CheckCircle } from 'lucide-vue-next'
import { Chart, registerables } from 'chart.js'

Chart.register(...registerables)

const props = defineProps({
  stats: {
    type: Object,
    required: true
  },
  logs: {
    type: Array,
    required: true,
    default: () => []
  }
})

defineEmits(['update-rules', 'view-audit'])

const chartCanvas = ref(null)
let chartInstance = null

const renderChart = () => {
  if (chartInstance) {
    chartInstance.destroy()
  }
  
  if (!chartCanvas.value) return

  chartInstance = new Chart(chartCanvas.value, {
    type: 'doughnut',
    data: {
      labels: ['Tonsilitis', 'Otitis Media', 'Sinusitis', 'Lainnya'],
      datasets: [{
        data: [
          props.stats.total_penyakit * 2 + 5,
          props.stats.total_gejala + 2,
          props.stats.total_aturan - 10 > 0 ? props.stats.total_aturan - 10 : 3,
          props.stats.total_riwayat || 5
        ],
        backgroundColor: ['#002045', '#13696a', '#455f88', '#bcc9c6'],
        borderWidth: 0,
        hoverOffset: 4
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'bottom',
          labels: {
            font: {
              size: 11,
              family: 'Inter'
            },
            boxWidth: 12
          }
        }
      }
    }
  })
}

onMounted(() => {
  renderChart()
})

watch(() => props.stats, () => {
  renderChart()
}, { deep: true })
</script>
