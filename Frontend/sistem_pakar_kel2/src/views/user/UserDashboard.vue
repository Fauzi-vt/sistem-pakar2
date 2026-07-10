<template>
  <UserLayout>
    <template v-if="loading">
      <SkeletonDashboard />
    </template>

    <template v-else>
      <AppBreadcrumb :items="[{ label: 'Dashboard' }]" />

      <!-- ── HEADER ── -->
      <header class="mb-6">
        <div class="flex flex-col sm:flex-row sm:items-end sm:justify-between gap-2">
          <div>
            <div class="flex items-center gap-2 mb-1">
              <Hand class="w-6 h-6 text-secondary shrink-0" />
              <h1 class="text-3xl font-bold text-primary leading-tight">
                Selamat Datang, {{ userName }}
              </h1>
            </div>
            <p class="text-on-surface-variant font-body-md pl-8">
              Sistem Pakar Diagnosis Penyakit THT
            </p>
          </div>
          <div class="flex items-center gap-1.5 text-on-surface-variant font-body-sm shrink-0 pl-8 sm:pl-0">
            <CalendarDays class="w-4 h-4" />
            <span>{{ todayLabel }}</span>
          </div>
        </div>
      </header>

      <!-- ── WELCOME CTA CARD ── -->
      <section
        class="bg-gradient-to-r from-primary to-primary-container text-on-primary rounded-2xl p-5 mb-6 flex flex-col sm:flex-row sm:items-center justify-between gap-4 shadow-sm transition-all duration-200 hover:shadow-lg hover:scale-[1.01]"
      >
        <div class="flex items-start gap-3">
          <Stethoscope class="w-6 h-6 mt-0.5 text-on-primary/80 shrink-0" />
          <div>
            <p class="font-bold text-base text-on-primary">
              {{ hasConsultedToday ? 'Konsultasi hari ini selesai!' : 'Anda belum konsultasi hari ini.' }}
            </p>
            <p class="text-on-primary/70 text-sm mt-0.5">
              <span v-if="stats.last_diagnosa">
                Terakhir konsultasi: {{ formatDate(stats.last_diagnosa.tanggal) }}
              </span>
              <span v-else>Mulai pemeriksaan pertama Anda sekarang.</span>
            </p>
          </div>
        </div>
        <button
          @click="$router.push('/user/diagnosa')"
          class="bg-white text-primary hover:bg-primary-fixed font-bold px-5 py-2.5 rounded-xl text-sm flex items-center gap-2 transition-all duration-200 active:scale-95 cursor-pointer shrink-0 self-start sm:self-center"
        >
          <Activity class="w-4 h-4" />
          Mulai Konsultasi
        </button>
      </section>

      <!-- ── QUICK STATS ── -->
      <section class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">

        <!-- Total Diagnosa -->
        <div class="bg-surface-container-lowest border border-outline-variant p-5 rounded-2xl flex items-center gap-4 transition-all duration-200 hover:shadow-lg hover:scale-[1.02] cursor-default">
          <div class="w-14 h-14 rounded-2xl bg-[#dce9ff] flex items-center justify-center shrink-0">
            <ClipboardList class="w-7 h-7 text-primary" />
          </div>
          <div>
            <p class="text-4xl font-bold text-primary leading-none">{{ stats.total_diagnosa }}</p>
            <p class="text-sm text-on-surface-variant mt-1">Total Diagnosa</p>
          </div>
        </div>

        <!-- Diagnosa Terakhir -->
        <div class="bg-surface-container-lowest border border-outline-variant p-5 rounded-2xl flex items-center gap-4 transition-all duration-200 hover:shadow-lg hover:scale-[1.02] cursor-default">
          <div class="w-14 h-14 rounded-2xl bg-secondary-container/50 flex items-center justify-center shrink-0">
            <History class="w-7 h-7 text-secondary" />
          </div>
          <div class="flex-1 min-w-0">
            <p
              v-if="stats.last_diagnosa"
              class="text-xl font-bold text-secondary leading-tight truncate"
            >{{ stats.last_diagnosa.penyakit }}</p>
            <p v-else class="text-xl font-bold text-outline leading-tight">—</p>
            <p class="text-sm text-on-surface-variant mt-1">Diagnosa Terakhir</p>
          </div>
        </div>

        <!-- Tanggal Bergabung -->
        <div class="bg-surface-container-lowest border border-outline-variant p-5 rounded-2xl flex items-center gap-4 transition-all duration-200 hover:shadow-lg hover:scale-[1.02] cursor-default">
          <div class="w-14 h-14 rounded-2xl bg-[#e8e6f4] flex items-center justify-center shrink-0">
            <CalendarCheck class="w-7 h-7 text-[#5b4e8a]" />
          </div>
          <div>
            <p class="text-base font-bold text-primary leading-tight">{{ joinDate }}</p>
            <p class="text-sm text-on-surface-variant mt-1">Tanggal Bergabung</p>
          </div>
        </div>

      </section>

      <!-- ── MAIN CONTENT ── -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">

        <!-- LEFT COLUMN -->
        <div class="lg:col-span-2 flex flex-col gap-6">

          <!-- Aksi Cepat (tanpa duplikat CTA konsultasi) -->
          <section class="bg-surface-container-low border border-outline-variant rounded-2xl p-6 transition-all duration-200 hover:shadow-md">
            <h2 class="text-lg font-bold text-primary mb-4 flex items-center gap-2">
              <Zap class="w-5 h-5 text-secondary" />
              Aksi Cepat
            </h2>
            <div class="flex flex-col sm:flex-row gap-3">
              <button
                @click="$router.push('/user/riwayat')"
                class="flex-1 bg-primary text-on-primary hover:bg-primary/90 p-4 rounded-xl font-bold flex items-center justify-center gap-2 transition-all duration-200 shadow-sm active:scale-95 cursor-pointer"
              >
                <ScrollText class="w-5 h-5" />
                Lihat Semua Riwayat
              </button>
              <button
                @click="$router.push('/user/profil')"
                class="flex-1 bg-surface-container-lowest border border-outline hover:border-primary text-primary p-4 rounded-xl font-bold flex items-center justify-center gap-2 transition-all duration-200 active:scale-95 cursor-pointer"
              >
                <UserCog class="w-5 h-5" />
                Kelola Profil
              </button>
            </div>
          </section>

          <!-- Mini Bar Chart — hanya tampil jika ≥10 diagnosa -->
          <section
            v-if="stats.total_diagnosa >= 10"
            class="bg-surface-container-lowest border border-outline-variant rounded-2xl p-6 transition-all duration-200 hover:shadow-md"
          >
            <div class="flex items-center justify-between mb-4">
              <h2 class="text-lg font-bold text-primary flex items-center gap-2">
                <BarChart3 class="w-5 h-5 text-secondary" />
                Aktivitas Diagnosa
              </h2>
              <span class="text-xs text-on-surface-variant">7 hari terakhir</span>
            </div>
            <div class="flex items-end gap-2 h-24">
              <div
                v-for="(bar, i) in weeklyBars"
                :key="i"
                class="flex-1 flex flex-col items-center gap-1"
              >
                <div
                  class="w-full rounded-t-lg transition-all duration-500"
                  :class="bar.active ? 'bg-primary' : 'bg-surface-container-high'"
                  :style="{ height: bar.height + 'px' }"
                  :title="bar.label + ': ' + bar.count + ' diagnosa'"
                ></div>
                <span class="text-[10px] text-on-surface-variant">{{ bar.label }}</span>
              </div>
            </div>
          </section>

          <!-- Riwayat Terakhir -->
          <section class="bg-surface-container-lowest border border-outline-variant rounded-2xl p-6 transition-all duration-200 hover:shadow-md">
            <div class="flex items-center justify-between mb-4">
              <h2 class="text-lg font-bold text-primary">Riwayat Terakhir</h2>
              <button
                @click="$router.push('/user/riwayat')"
                class="text-secondary text-sm font-medium hover:underline cursor-pointer"
              >Lihat Semua</button>
            </div>

            <!-- Empty State -->
            <div
              v-if="recentDiagnoses.length === 0"
              class="flex flex-col items-center py-10 gap-3"
            >
              <div class="w-16 h-16 rounded-full bg-surface-container flex items-center justify-center">
                <Stethoscope class="w-8 h-8 text-outline" />
              </div>
              <p class="font-semibold text-on-surface-variant">Belum ada riwayat diagnosa</p>
              <p class="text-sm text-outline text-center">Mulai diagnosa pertama Anda untuk melihat hasil analisa kesehatan THT.</p>
              <button
                @click="$router.push('/user/diagnosa')"
                class="mt-2 bg-primary text-on-primary px-5 py-2 rounded-xl text-sm font-bold flex items-center gap-2 hover:bg-primary/90 transition-all cursor-pointer active:scale-95"
              >
                <Activity class="w-4 h-4" />
                Mulai Sekarang
              </button>
            </div>

            <!-- List -->
            <div v-else class="flex flex-col gap-3">
              <div
                v-for="item in recentDiagnoses"
                :key="item.id"
                class="p-4 rounded-xl border border-outline-variant/60 hover:bg-surface-container-low transition-all duration-200 hover:shadow-sm group"
              >
                <!-- Row atas: nama + badge -->
                <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                  <div class="flex items-center gap-3">
                    <div class="w-9 h-9 rounded-full bg-primary-container/30 flex items-center justify-center shrink-0">
                      <Microscope class="w-4 h-4 text-primary" />
                    </div>
                    <div>
                      <p class="font-bold text-primary text-base leading-tight">{{ item.penyakit }}</p>
                      <div class="flex items-center gap-1.5 mt-0.5 text-xs text-on-surface-variant">
                        <CalendarDays class="w-3 h-3" />
                        <span>{{ formatDate(item.tanggal) }}</span>
                      </div>
                    </div>
                  </div>
                  <div class="flex items-center gap-3 shrink-0">
                    <span
                      class="px-2.5 py-1 rounded-full text-xs font-semibold"
                      :class="probabilityBadge(item.persentase).cls"
                    >{{ probabilityBadge(item.persentase).label }}</span>
                    <button
                      @click="$router.push('/user/riwayat')"
                      class="w-8 h-8 rounded-full bg-surface-container flex items-center justify-center text-primary hover:bg-secondary-container transition-colors cursor-pointer"
                    >
                      <ArrowRight class="w-4 h-4" />
                    </button>
                  </div>
                </div>

                <!-- Progress Bar -->
                <div class="mt-3">
                  <div class="flex items-center justify-between mb-1">
                    <span class="text-xs text-on-surface-variant">Probabilitas</span>
                    <span
                      class="text-xs font-bold"
                      :class="probabilityBadge(item.persentase).textCls"
                    >{{ Number(item.persentase || 0).toFixed(2) }}%</span>
                  </div>
                  <div class="h-1.5 bg-surface-container-high rounded-full overflow-hidden">
                    <div
                      class="h-full rounded-full transition-all duration-700"
                      :class="probabilityBadge(item.persentase).barCls"
                      :style="{ width: item.persentase + '%' }"
                    ></div>
                  </div>
                </div>
              </div>
            </div>
          </section>

        </div>

        <!-- RIGHT COLUMN -->
        <div class="flex flex-col gap-6">

          <!-- Metode Sistem -->
          <section class="bg-surface-container-lowest border border-outline-variant rounded-2xl p-6 transition-all duration-200 hover:shadow-md">
            <h2 class="text-lg font-bold text-primary mb-4 flex items-center gap-2">
              <Brain class="w-5 h-5 text-secondary" />
              Metode Sistem
            </h2>
            <ul class="flex flex-col gap-3">
              <li class="flex items-start gap-3">
                <div class="w-5 h-5 rounded-full bg-secondary-container flex items-center justify-center shrink-0 mt-0.5">
                  <Check class="w-3 h-3 text-secondary" />
                </div>
                <span class="text-sm text-on-surface-variant leading-relaxed">
                  Menggunakan <strong class="text-primary">sistem pakar berbasis probabilitas</strong> sebagai algoritma inti
                </span>
              </li>
              <li class="flex items-start gap-3">
                <div class="w-5 h-5 rounded-full bg-secondary-container flex items-center justify-center shrink-0 mt-0.5">
                  <Check class="w-3 h-3 text-secondary" />
                </div>
                <span class="text-sm text-on-surface-variant leading-relaxed">
                  Probabilitas dihitung berdasarkan gejala yang dipilih
                </span>
              </li>
              <li class="flex items-start gap-3">
                <div class="w-5 h-5 rounded-full bg-secondary-container flex items-center justify-center shrink-0 mt-0.5">
                  <Check class="w-3 h-3 text-secondary" />
                </div>
                <span class="text-sm text-on-surface-variant leading-relaxed">
                  Menampilkan estimasi awal penyakit THT secara probabilistik
                </span>
              </li>
            </ul>
          </section>

          <!-- Disclaimer — amber -->
          <section class="bg-amber-50 border border-amber-200 rounded-2xl p-6 transition-all duration-200 hover:shadow-md">
            <h2 class="text-base font-bold text-amber-700 mb-2 flex items-center gap-2">
              <TriangleAlert class="w-5 h-5 text-amber-500" />
              Disclaimer Medis
            </h2>
            <p class="text-sm text-amber-800/80 leading-relaxed">
              Hasil diagnosa dari sistem ini bertujuan sebagai
              <strong>informasi awal</strong> dan edukasi. Hasil ini
              <strong>TIDAK DAPAT</strong> menggantikan diagnosis langsung, nasihat medis, maupun
              resep dari dokter spesialis THT. Segera konsultasikan ke fasilitas kesehatan jika gejala memburuk.
            </p>
          </section>

        </div>

      </div>
    </template>
  </UserLayout>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import {
  Hand, CalendarDays, Stethoscope, Activity, ClipboardList,
  History, CalendarCheck, Zap, ScrollText, UserCog, BarChart3,
  Microscope, ArrowRight, Brain, Check, TriangleAlert
} from 'lucide-vue-next'

import { useAuthStore }    from '@/stores/auth.store'
import { useRiwayatStore } from '@/stores/riwayat.store'
import UserLayout          from '@/layouts/UserLayout.vue'
import AppBreadcrumb       from '@/components/common/AppBreadcrumb.vue'
import SkeletonDashboard   from '@/components/common/SkeletonDashboard.vue'

const authStore    = useAuthStore()
const riwayatStore = useRiwayatStore()

// ── User info ──────────────────────────────────────────────────────────────
const userName = computed(() => {
  if (!authStore.currentUser?.name) return 'Pengguna'
  const first = authStore.currentUser.name.split(' ')[0]
  return first.charAt(0).toUpperCase() + first.slice(1)
})

const joinDate = computed(() => {
  if (!authStore.currentUser?.created_at) return '—'
  return new Date(authStore.currentUser.created_at).toLocaleDateString('id-ID', {
    day: 'numeric', month: 'long', year: 'numeric'
  })
})

// ── Tanggal hari ini ───────────────────────────────────────────────────────
const todayLabel = computed(() => {
  return new Date().toLocaleDateString('id-ID', {
    weekday: 'long', day: 'numeric', month: 'long', year: 'numeric'
  })
})

// ── Store data ─────────────────────────────────────────────────────────────
const loading         = computed(() => riwayatStore.loading)
const recentDiagnoses = computed(() => riwayatStore.recentList)
const stats           = computed(() => ({
  total_diagnosa: riwayatStore.riwayatList.length,
  last_diagnosa:  riwayatStore.riwayatList.length > 0 ? riwayatStore.riwayatList[0] : null
}))

// ── Sudah konsultasi hari ini? ─────────────────────────────────────────────
const hasConsultedToday = computed(() => {
  if (!stats.value.last_diagnosa) return false
  const today   = new Date().toDateString()
  const lastDate = new Date(stats.value.last_diagnosa.tanggal).toDateString()
  return today === lastDate
})

// ── Mini bar chart (7 hari terakhir) ──────────────────────────────────────
const weeklyBars = computed(() => {
  const days   = ['Min', 'Sen', 'Sel', 'Rab', 'Kam', 'Jum', 'Sab']
  const counts = Array(7).fill(0)
  const today  = new Date()

  riwayatStore.riwayatList.forEach(r => {
    const d    = new Date(r.tanggal)
    const diff = Math.floor((today - d) / 86400000)
    if (diff >= 0 && diff < 7) {
      counts[6 - diff]++
    }
  })

  const max = Math.max(...counts, 1)
  const MAX_H = 72 // px

  return counts.map((count, i) => {
    const dayIndex = (today.getDay() - (6 - i) + 7) % 7
    return {
      label:  days[dayIndex],
      count,
      height: Math.max(6, Math.round((count / max) * MAX_H)),
      active: count > 0
    }
  })
})

// ── Badge probabilitas ─────────────────────────────────────────────────────
const probabilityBadge = (persen) => {
  if (persen >= 80) return {
    label:   'Probabilitas Tinggi',
    cls:     'bg-emerald-100 text-emerald-700',
    textCls: 'text-emerald-600',
    barCls:  'bg-emerald-500'
  }
  if (persen >= 50) return {
    label:   'Probabilitas Sedang',
    cls:     'bg-amber-100 text-amber-700',
    textCls: 'text-amber-600',
    barCls:  'bg-amber-400'
  }
  return {
    label:   'Probabilitas Rendah',
    cls:     'bg-surface-container text-on-surface-variant',
    textCls: 'text-outline',
    barCls:  'bg-outline'
  }
}

// ── Format tanggal ─────────────────────────────────────────────────────────
const formatDate = (dateString) => {
  if (!dateString) return '-'
  return new Date(dateString).toLocaleDateString('id-ID', {
    day: 'numeric', month: 'long', year: 'numeric'
  })
}

// ── Fetch data ─────────────────────────────────────────────────────────────
onMounted(async () => {
  if (authStore.currentUser?.id) {
    await riwayatStore.fetchByUser(authStore.currentUser.id)
  }
})
</script>
