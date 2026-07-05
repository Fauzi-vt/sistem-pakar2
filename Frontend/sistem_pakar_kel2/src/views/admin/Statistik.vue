<template>
  <div class="min-h-screen bg-background text-on-background font-body-md flex relative antialiased">
    <!-- Side Navigation -->
    <Sidebar v-model:isOpen="sidebarOpen" />

    <!-- Main Content Area -->
    <div class="flex-1 flex flex-col min-h-screen lg:ml-64 transition-all duration-300">

      <!-- Top Navigation Header -->
      <header class="bg-surface-container-lowest dark:bg-surface-container flex justify-between items-center w-full px-container-padding h-16 sticky top-0 z-40 border-b border-outline-variant">
        <div class="flex items-center gap-4 w-full lg:w-1/2">
          <button @click="sidebarOpen = !sidebarOpen"
                  class="lg:hidden flex items-center justify-center p-2 bg-surface-container rounded-lg text-on-surface hover:bg-surface-container-high transition-colors">
            <span class="material-symbols-outlined">menu</span>
          </button>
          <div>
            <h1 class="font-headline-sm text-headline-sm font-bold text-primary truncate leading-tight">Statistik Diagnosa</h1>
            <p class="text-xs text-on-surface-variant hidden sm:block mt-0.5">Analisis komprehensif hasil pemeriksaan klinis Bayes</p>
          </div>
        </div>
        <!-- Refresh Button -->
        <button @click="fetchStatistik"
                :disabled="loading"
                class="flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs font-semibold text-secondary border border-secondary/30 hover:bg-secondary/10 transition-all disabled:opacity-50 cursor-pointer">
          <RefreshCw class="w-3.5 h-3.5" :class="{ 'animate-spin': loading }" />
          <span class="hidden sm:inline">Perbarui Data</span>
        </button>
      </header>

      <!-- Main Canvas -->
      <main class="p-container-padding flex-1 flex flex-col gap-stack-lg">

        <!-- Error Banner -->
        <div v-if="error"
             class="flex items-center gap-3 p-4 bg-error-container text-on-error-container rounded-lg border border-error/20">
          <AlertCircle class="w-5 h-5 shrink-0" />
          <p class="text-sm font-medium">{{ error }}</p>
          <button @click="fetchStatistik" class="ml-auto text-xs underline font-bold cursor-pointer">Coba lagi</button>
        </div>

        <!-- Loading Skeleton -->
        <template v-if="loading">
          <div class="grid grid-cols-2 md:grid-cols-4 gap-gutter">
            <div v-for="i in 4" :key="i" class="bg-surface-container-lowest border border-outline-variant rounded-xl p-5 animate-pulse">
              <div class="h-3 w-24 bg-surface-container-high rounded mb-3"></div>
              <div class="h-8 w-16 bg-surface-container-high rounded"></div>
            </div>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-gutter">
            <div v-for="i in 4" :key="i" class="bg-surface-container-lowest border border-outline-variant rounded-xl p-6 h-64 animate-pulse"></div>
          </div>
        </template>

        <!-- Content -->
        <template v-else>

          <!-- ── Summary Cards ──────────────────────────────── -->
          <div class="grid grid-cols-2 md:grid-cols-4 gap-gutter">

            <div class="stat-card group">
              <div class="flex items-start justify-between">
                <div>
                  <p class="stat-label">Total Diagnosa</p>
                  <p class="stat-value text-primary">{{ summary.total_diagnosa }}</p>
                </div>
                <div class="stat-icon bg-primary/10 text-primary">
                  <ClipboardList class="w-5 h-5" />
                </div>
              </div>
              <p class="stat-sub">{{ summary.total_valid }} berhasil diproses</p>
            </div>

            <div class="stat-card group">
              <div class="flex items-start justify-between">
                <div>
                  <p class="stat-label">Rata-rata Keyakinan</p>
                  <p class="stat-value text-secondary">{{ summary.rata_rata_keyakinan?.toFixed(1) ?? '0.0' }}%</p>
                </div>
                <div class="stat-icon bg-secondary/10 text-secondary">
                  <TrendingUp class="w-5 h-5" />
                </div>
              </div>
              <p class="stat-sub">Probabilitas posterior Bayes</p>
            </div>

            <div class="stat-card group">
              <div class="flex items-start justify-between">
                <div>
                  <p class="stat-label">Penyakit Terbanyak</p>
                  <p class="stat-value text-primary text-lg leading-snug truncate max-w-[120px]">{{ summary.penyakit_terbanyak ?? '-' }}</p>
                </div>
                <div class="stat-icon bg-tertiary/10 text-tertiary">
                  <Activity class="w-5 h-5" />
                </div>
              </div>
              <p class="stat-sub">Diagnosis paling sering muncul</p>
            </div>

            <div class="stat-card group">
              <div class="flex items-start justify-between">
                <div>
                  <p class="stat-label">Gejala Terbanyak</p>
                  <p class="stat-value text-primary text-lg leading-snug truncate max-w-[120px]">{{ summary.gejala_terbanyak ?? '-' }}</p>
                </div>
                <div class="stat-icon bg-error/10 text-error">
                  <HeartPulse class="w-5 h-5" />
                </div>
              </div>
              <p class="stat-sub">Gejala paling sering dipilih</p>
            </div>
          </div>

          <!-- ── Charts Row ─────────────────────────────────── -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-gutter">

            <!-- Distribusi Penyakit -->
            <div class="chart-card">
              <div class="chart-header">
                <div>
                  <h3 class="chart-title">Distribusi Penyakit</h3>
                  <p class="chart-sub">Frekuensi diagnosis per penyakit (top 10)</p>
                </div>
                <span class="badge badge-primary">{{ diseaseDistribution.length }} Penyakit</span>
              </div>
              <div v-if="diseaseDistribution.length === 0" class="empty-state">
                <BarChart2 class="w-10 h-10 opacity-30" />
                <p>Belum ada data diagnosis</p>
              </div>
              <div v-else class="space-y-3 mt-1">
                <div v-for="(d, idx) in diseaseDistribution" :key="d.name" class="space-y-1">
                  <div class="flex justify-between items-center text-xs font-semibold">
                    <span class="flex items-center gap-1.5 text-on-surface">
                      <span class="rank-badge">{{ idx + 1 }}</span>
                      {{ d.name }}
                    </span>
                    <span class="text-on-surface-variant font-bold font-mono">{{ d.count }} <span class="text-outline font-normal">({{ d.pct }}%)</span></span>
                  </div>
                  <div class="w-full bg-surface-container rounded-full h-2 overflow-hidden">
                    <div class="h-2 rounded-full transition-all duration-700"
                         :class="getBarColor(idx)"
                         :style="{ width: `${d.pct}%` }"></div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Tingkat Keyakinan Bayes -->
            <div class="chart-card">
              <div class="chart-header">
                <div>
                  <h3 class="chart-title">Tingkat Keyakinan Inferensi</h3>
                  <p class="chart-sub">Distribusi probabilitas posterior Bayes</p>
                </div>
                <span class="badge badge-secondary">{{ summary.total_valid }} Kasus</span>
              </div>
              <div v-if="!summary.total_valid" class="empty-state">
                <PieChart class="w-10 h-10 opacity-30" />
                <p>Belum ada data keyakinan</p>
              </div>
              <div v-else class="space-y-4 mt-2">
                <div v-for="s in confidenceDistribution" :key="s.range" class="space-y-1.5">
                  <div class="flex justify-between items-center text-xs">
                    <div class="flex items-center gap-2">
                      <span class="w-2.5 h-2.5 rounded-full shrink-0" :class="getConfidenceColor(s.range)"></span>
                      <span class="font-semibold text-on-surface">{{ s.range }}</span>
                    </div>
                    <span class="font-bold text-on-surface-variant font-mono">
                      {{ s.count }} pasien
                      <span class="text-outline font-normal">({{ s.pct }}%)</span>
                    </span>
                  </div>
                  <div class="w-full bg-surface-container rounded-full h-3 overflow-hidden">
                    <div class="h-3 rounded-full transition-all duration-700"
                         :class="getConfidenceBg(s.range)"
                         :style="{ width: `${s.pct}%` }">
                    </div>
                  </div>
                </div>
              </div>

              <!-- Mini donut visual -->
              <div v-if="summary.total_valid" class="flex gap-3 mt-4 flex-wrap">
                <div v-for="s in confidenceDistribution" :key="s.range + '_dot'"
                     class="flex items-center gap-1.5 text-[11px] text-on-surface-variant">
                  <span class="w-2 h-2 rounded-full shrink-0" :class="getConfidenceColor(s.range)"></span>
                  {{ s.pct }}%
                </div>
              </div>
            </div>

            <!-- Tren Bulanan -->
            <div class="chart-card">
              <div class="chart-header">
                <div>
                  <h3 class="chart-title">Tren Diagnosa Bulanan</h3>
                  <p class="chart-sub">Jumlah diagnosa per bulan (12 bulan terakhir)</p>
                </div>
                <span class="badge badge-tertiary">{{ monthlyTrend.length }} Bulan</span>
              </div>
              <div v-if="monthlyTrend.length === 0" class="empty-state">
                <TrendingUp class="w-10 h-10 opacity-30" />
                <p>Belum ada data tren</p>
              </div>
              <div v-else class="mt-3">
                <!-- Bar chart visual -->
                <div class="flex items-end gap-1.5 h-28 w-full">
                  <div v-for="m in monthlyTrend" :key="m.month"
                       class="flex-1 flex flex-col items-center justify-end gap-1 group/bar cursor-default">
                    <span class="text-[9px] font-bold text-primary opacity-0 group-hover/bar:opacity-100 transition-opacity">{{ m.count }}</span>
                    <div class="w-full rounded-t-sm bg-primary/80 hover:bg-primary transition-all duration-300"
                         :style="{ height: `${getBarHeight(m.count)}px` }"
                         :title="`${formatMonth(m.month)}: ${m.count} diagnosa`">
                    </div>
                  </div>
                </div>
                <!-- Month labels -->
                <div class="flex gap-1.5 mt-1.5">
                  <div v-for="m in monthlyTrend" :key="m.month + '_lbl'" class="flex-1 text-center">
                    <span class="text-[9px] text-on-surface-variant">{{ formatMonthShort(m.month) }}</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Frekuensi Gejala -->
            <div class="chart-card">
              <div class="chart-header">
                <div>
                  <h3 class="chart-title">Gejala Paling Sering</h3>
                  <p class="chart-sub">Gejala yang paling banyak dipilih pasien (top 10)</p>
                </div>
                <span class="badge badge-error">{{ symptomFrequency.length }} Gejala</span>
              </div>
              <div v-if="symptomFrequency.length === 0" class="empty-state">
                <Activity class="w-10 h-10 opacity-30" />
                <p>Belum ada data gejala</p>
              </div>
              <div v-else class="space-y-2.5 mt-1">
                <div v-for="(s, idx) in symptomFrequency" :key="s.name" class="flex items-center gap-3">
                  <span class="text-[10px] font-bold text-on-surface-variant font-mono w-5 text-right shrink-0">{{ idx + 1 }}</span>
                  <div class="flex-1 min-w-0">
                    <div class="flex justify-between items-center mb-0.5">
                      <span class="text-xs font-semibold text-on-surface truncate">{{ s.name }}</span>
                      <span class="text-xs font-bold text-error shrink-0 ml-2">{{ s.count }}x</span>
                    </div>
                    <div class="w-full bg-surface-container rounded-full h-1.5 overflow-hidden">
                      <div class="h-1.5 rounded-full bg-error/70 transition-all duration-700"
                           :style="{ width: `${getSymptomPct(s.count)}%` }">
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

          </div>

        </template>

      </main>

      <!-- Footer -->
      <footer class="border-t border-outline-variant px-6 py-4 bg-surface-container-lowest shrink-0">
        <p class="text-on-surface-variant text-xs text-center">© 2026 Sistem Pakar THT — Kelompok 2 · RS Jasa Kartini. All rights reserved.</p>
      </footer>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { api } from '@/services/api'
import Sidebar from '../../components/Sidebar.vue'
import {
  RefreshCw, AlertCircle, ClipboardList, TrendingUp, Activity,
  HeartPulse, BarChart2, PieChart
} from 'lucide-vue-next'

const sidebarOpen = ref(false)
const loading     = ref(true)
const error       = ref(null)

// Data dari API
const summary              = ref({ total_diagnosa: 0, total_valid: 0, rata_rata_keyakinan: 0, penyakit_terbanyak: '-', gejala_terbanyak: '-' })
const diseaseDistribution  = ref([])
const confidenceDistribution = ref([])
const monthlyTrend         = ref([])
const symptomFrequency     = ref([])

// ── Fetch ──────────────────────────────────────────────
const fetchStatistik = async () => {
  loading.value = true
  error.value   = null
  try {
    const res = await api.getStatistikDiagnosa()
    if (res.success) {
      summary.value              = res.summary              || summary.value
      diseaseDistribution.value  = res.disease_distribution || []
      confidenceDistribution.value = res.confidence_distribution || []
      monthlyTrend.value         = res.monthly_trend        || []
      symptomFrequency.value     = res.symptom_frequency    || []
    }
  } catch (err) {
    error.value = 'Gagal memuat statistik: ' + (err.message || 'Terjadi kesalahan pada server.')
  } finally {
    loading.value = false
  }
}

onMounted(fetchStatistik)

// ── Helpers ────────────────────────────────────────────
const DISEASE_COLORS = [
  'bg-primary', 'bg-secondary', 'bg-tertiary',
  'bg-primary/70', 'bg-secondary/70', 'bg-tertiary/70',
  'bg-primary/50', 'bg-secondary/50', 'bg-tertiary/50', 'bg-error/60'
]
const getBarColor = (idx) => DISEASE_COLORS[idx % DISEASE_COLORS.length]

const getConfidenceColor = (range) => {
  if (range.startsWith('>= 80')) return 'bg-[#1E8E3E]'
  if (range.startsWith('60'))    return 'bg-secondary'
  if (range.startsWith('40'))    return 'bg-[#B06000]'
  return 'bg-error'
}
const getConfidenceBg = (range) => {
  if (range.startsWith('>= 80')) return 'bg-[#1E8E3E]'
  if (range.startsWith('60'))    return 'bg-secondary'
  if (range.startsWith('40'))    return 'bg-[#B06000]'
  return 'bg-error'
}

const maxMonthly = computed(() => Math.max(...monthlyTrend.value.map(m => m.count), 1))
const getBarHeight = (count) => Math.max(4, Math.round((count / maxMonthly.value) * 96))

const maxSymptom = computed(() => Math.max(...symptomFrequency.value.map(s => s.count), 1))
const getSymptomPct = (count) => Math.round((count / maxSymptom.value) * 100)

const formatMonth = (ym) => {
  try {
    const [y, m] = ym.split('-')
    return new Date(parseInt(y), parseInt(m) - 1).toLocaleDateString('id-ID', { month: 'long', year: 'numeric' })
  } catch { return ym }
}
const formatMonthShort = (ym) => {
  try {
    const [y, m] = ym.split('-')
    return new Date(parseInt(y), parseInt(m) - 1).toLocaleDateString('id-ID', { month: 'short' })
  } catch { return ym }
}
</script>

<style scoped>
.stat-card {
  background: var(--color-surface-container-lowest, #fff);
  border: 1px solid var(--color-outline-variant, #e0e0e0);
  border-radius: 0.75rem;
  padding: 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  transition: all 0.2s;
}
.stat-card:hover {
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}
.stat-label {
  font-size: 0.7rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--color-on-surface-variant, #666);
}
.stat-value {
  font-size: 1.875rem;
  font-weight: 700;
  margin-top: 0.25rem;
}
.stat-sub {
  font-size: 0.7rem;
  color: var(--color-on-surface-variant, #666);
}
.stat-icon {
  padding: 0.5rem;
  border-radius: 0.5rem;
  flex-shrink: 0;
}

.chart-card {
  background: var(--color-surface-container-lowest, #fff);
  border: 1px solid var(--color-outline-variant, #e0e0e0);
  border-radius: 0.75rem;
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}
.chart-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 0.5rem;
}
.chart-title {
  font-weight: 700;
  font-size: 0.875rem;
  color: var(--color-primary, #1a365d);
}
.chart-sub {
  font-size: 0.7rem;
  color: var(--color-on-surface-variant, #666);
  margin-top: 0.125rem;
}

.badge {
  padding: 0.25rem 0.625rem;
  border-radius: 9999px;
  font-size: 0.65rem;
  font-weight: 700;
  white-space: nowrap;
  flex-shrink: 0;
}
.badge-primary  { background: rgba(var(--color-primary-rgb, 26,54,93), 0.1); color: var(--color-primary, #1a365d); }
.badge-secondary { background: rgba(var(--color-secondary-rgb, 74,144,226), 0.1); color: var(--color-secondary, #4a90e2); }
.badge-tertiary { background: rgba(98,196,165,0.1); color: #2e7d62; }
.badge-error    { background: rgba(var(--color-error-rgb, 211,47,47), 0.1); color: var(--color-error, #d32f2f); }

.rank-badge {
  font-size: 0.625rem;
  font-weight: 700;
  background: var(--color-surface-container, #f5f5f5);
  color: var(--color-on-surface-variant, #666);
  width: 1rem;
  height: 1rem;
  border-radius: 0.25rem;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2.5rem 1rem;
  gap: 0.5rem;
  color: var(--color-on-surface-variant, #888);
  font-size: 0.875rem;
}
</style>

