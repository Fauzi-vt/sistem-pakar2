<template>
  <UserLayout>
    <AppBreadcrumb :items="[{ label: 'Dashboard', to: '/user/dashboard' }, { label: 'Konsultasi' }]" />
    
    <FullScreenLoader 
      :isVisible="isLoading" 
      title="Memproses Diagnosa" 
      message="Sistem sedang menghitung probabilitas berdasarkan gejala Anda..." 
    />

    <!-- Main Content -->
    <div class="max-w-5xl mx-auto py-4">
      <Transition name="page-slide" mode="out-in">
        
        <!-- ════ STEP 1 — Symptom Selection ════ -->
        <div v-if="!diagnosaResult" key="step1">
          <header class="mb-8 mt-2">
            <h1 class="text-4xl font-extrabold text-[#0b1c30] flex items-center gap-3 mb-2">
              <Stethoscope class="w-10 h-10 text-[#00685f]" />
              Checklist Gejala
            </h1>
            <p class="text-sm text-[#3d4947] ml-13">Pilih gejala yang sedang Anda alami.</p>
          </header>

          <!-- Loading state -->
          <div v-if="loadingGejala" class="bg-white rounded-xl border border-[#bcc9c6]/30 p-12 text-center shadow-[0px_4px_20px_rgba(15,23,42,0.05)]">
            <div class="flex items-center justify-center gap-2">
              <span class="w-4 h-4 border-2 border-t-transparent rounded-full animate-spin border-[#00685f]"></span>
              <span class="text-sm font-semibold text-[#6d7a77]">Memuat daftar gejala...</span>
            </div>
          </div>

          <!-- Error state -->
          <div v-else-if="fetchError" class="bg-white rounded-xl border border-[#bcc9c6]/30 p-8 text-center shadow-[0px_4px_20px_rgba(15,23,42,0.05)]">
            <p class="text-sm font-semibold text-[#ba1a1a] mb-3">Gagal memuat gejala: {{ fetchError }}</p>
            <button @click="fetchGejala" class="bg-[#00685f] text-white hover:bg-[#005049] px-4 py-2 rounded-lg text-xs font-semibold transition-colors cursor-pointer">
              Coba Lagi
            </button>
          </div>

          <form v-else class="bg-white rounded-xl border border-[#bcc9c6]/30 p-6 md:p-8 shadow-[0px_4px_20px_rgba(15,23,42,0.05)] space-y-4">
            <!-- Progress Indicator -->
            <div class="mb-4">
              <div class="flex justify-between items-end mb-2">
                <span class="text-xs font-bold uppercase tracking-wider text-[#6d7a77]">Progress</span>
                <span class="text-xs font-semibold text-[#00685f]">
                  {{ selectedGejala.length }} / {{ gejalaList.length }} Gejala Dipilih
                </span>
              </div>
              <div class="w-full bg-[#e5eeff] rounded-full h-2.5 overflow-hidden">
                <div class="bg-[#00685f] h-full rounded-full transition-all duration-300 ease-out" 
                     :style="{ width: gejalaList.length > 0 ? `${(selectedGejala.length / gejalaList.length) * 100}%` : '0%' }">
                </div>
              </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <!-- Checklist Items -->
              <label v-for="item in gejalaList" :key="item.id"
                     class="flex items-center p-4 rounded-xl cursor-pointer border transition-all duration-200 group hover:shadow-sm hover:scale-[1.01]"
                     :class="selectedGejala.includes(item.id) ? 'border-[#00685f] bg-[#e0f2f1]' : 'border-[#bcc9c6]/50 bg-white hover:border-[#00685f]/50'">
                
                <div class="flex items-center h-full mr-3 shrink-0">
                  <input class="w-5 h-5 text-[#00685f] border-[#bcc9c6] rounded focus:ring-[#00685f]/50 focus:ring-offset-0 bg-white cursor-pointer transition-colors" 
                         type="checkbox"
                         :value="item.id"
                         v-model="selectedGejala"/>
                </div>
                
                <div class="flex items-center gap-3 flex-1 min-w-0">
                  <div class="w-10 h-10 rounded-lg flex items-center justify-center shrink-0 transition-colors"
                       :class="selectedGejala.includes(item.id) ? 'bg-[#00685f] text-white' : 'bg-[#e5eeff] text-[#00685f] group-hover:bg-[#00685f]/10'">
                    <component :is="getSymptomIconComponent(item.nama)" class="w-5 h-5" />
                  </div>
                  
                  <div class="flex-1 min-w-0">
                    <span class="text-sm font-bold text-[#0b1c30] block mb-0.5 truncate transition-colors"
                          :class="selectedGejala.includes(item.id) ? 'text-[#005049]' : 'group-hover:text-[#00685f]'">
                      {{ item.nama }}
                    </span>
                    <span class="text-[11px] text-[#3d4947] font-medium" :class="selectedGejala.includes(item.id) ? 'text-[#00685f]/80' : ''">
                      Kode: {{ item.kode }}
                    </span>
                  </div>
                </div>
              </label>
            </div>

            <!-- Error message on submit -->
            <Transition name="slide-down">
              <div v-if="diagnosaError" class="p-3 text-xs text-[#93000a] bg-[#ffdad6] border border-[#ba1a1a]/20 rounded-lg">
                {{ diagnosaError }}
              </div>
            </Transition>

            <div class="flex items-center justify-between border-t border-[#bcc9c6]/30 pt-6 mt-6">
              <button @click="resetDiagnosa" 
                      type="button"
                      class="text-[#3d4947] hover:text-[#ba1a1a] text-xs font-bold py-2.5 px-4 rounded-lg hover:bg-[#ffdad6]/50 transition-colors flex items-center cursor-pointer">
                Reset
              </button>
              
              <button @click="handleDiagnosa" 
                      :disabled="selectedGejala.length === 0 || isLoading"
                      class="bg-[#00685f] hover:bg-[#006a61] text-white text-xs font-bold py-3 px-8 rounded-lg shadow-sm transition-all flex items-center justify-center min-h-[44px] active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer" 
                      type="button">
                <span v-if="isLoading" class="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin mr-2"></span>
                <span>Diagnosa Sekarang</span>
                <ArrowRight class="ml-2 w-4 h-4 text-white" />
              </button>
            </div>
          </form>
        </div>

        <!-- ════ STEP 2 — Diagnosis Result ════ -->
        <div v-else key="step2" class="space-y-6 animate-page-slide">
          <header class="mb-6 text-center md:text-left">
            <h1 class="text-3xl font-bold text-[#0b1c30] mb-2">Hasil Diagnosis</h1>
            <p class="text-sm text-[#3d4947]">Berdasarkan gejala yang Anda masukkan, berikut adalah probabilitas penyakit yang mungkin Anda alami.</p>
          </header>

          <!-- No matched result -->
          <div v-if="!topResult" class="bg-white rounded-xl border border-[#bcc9c6]/30 p-12 text-center shadow-[0px_4px_20px_rgba(15,23,42,0.05)]">
            <p class="font-bold text-[#0b1c30] mb-2">Tidak Ada Hasil Diagnosa</p>
            <p class="text-xs text-[#6d7a77] mb-6">Sistem tidak menemukan penyakit yang cocok dengan gejala yang Anda pilih.</p>
            <button @click="resetDiagnosa" class="bg-[#00685f] text-white hover:bg-[#005049] px-6 py-2.5 rounded-lg text-xs font-semibold cursor-pointer">
              Coba Lagi
            </button>
          </div>

          <!-- Has result -->
          <div v-else class="space-y-6">
            <!-- Primary Diagnosis Card -->
            <div class="bg-white rounded-xl shadow-md border border-[#bcc9c6]/30 p-6 md:p-8 relative overflow-hidden">
              <!-- Decorative accent -->
              <div class="absolute top-0 left-0 w-2 h-full bg-[#00685f]"></div>
              
              <div class="flex flex-col md:flex-row md:items-start justify-between gap-6">
                <div class="flex-1 space-y-6">
                  
                  <div class="flex items-center gap-2 mb-4">
                    <Stethoscope class="text-[#00685f] w-6 h-6" />
                    <h2 class="text-2xl font-bold text-[#00685f]">{{ topResult.nama_penyakit }}</h2>
                  </div>

                  <div class="mb-6">
                    <div class="flex justify-between items-end mb-2">
                      <span class="text-xs font-semibold text-[#3d4947]">Tingkat Keyakinan</span>
                      <div class="flex items-baseline gap-2">
                        <span class="text-2xl font-extrabold text-[#00685f]">{{ topResult.persentase.toFixed(2) }}%</span>
                        <span class="text-[10px] font-bold text-[#005049] bg-[#e0f2f1] px-2 py-0.5 rounded-full">
                          {{ topResult.status }}
                        </span>
                      </div>
                    </div>
                    <div class="w-full bg-[#e5eeff] rounded-full h-2">
                      <div class="bg-[#00685f] h-2 rounded-full transition-all duration-1000" :style="{ width: `${Math.min(topResult.persentase, 100)}%` }"></div>
                    </div>
                  </div>

                  <div class="space-y-6">
                    <!-- Deskripsi -->
                    <div>
                      <h3 class="text-base font-bold text-[#0b1c30] mb-2 flex items-center gap-2">
                        <FileText class="text-[#006387] w-5 h-5" />
                        <span>Deskripsi Penyakit</span>
                      </h3>
                      <p class="text-sm leading-relaxed text-[#3d4947]">
                        {{ topResult.deskripsi || 'Belum ada penjelasan deskriptif yang tersedia untuk penyakit ini.' }}
                      </p>
                    </div>

                    <!-- Saran Medis -->
                    <div>
                      <h3 class="text-base font-bold text-[#0b1c30] mb-2 flex items-center gap-2">
                        <HeartPulse class="text-[#006387] w-5 h-5" />
                        <span>Saran Medis / Solusi</span>
                      </h3>
                      <ul v-if="solutionsList.length > 0" class="text-sm leading-relaxed text-[#3d4947] list-disc list-inside space-y-1">
                        <li v-for="sol in solutionsList" :key="sol">{{ sol }}</li>
                      </ul>
                      <p v-else class="text-sm text-[#6d7a77] italic">Rekomendasi penanganan klinis sedang dipersiapkan oleh tim spesialis.</p>
                    </div>



                  </div>

                </div>
              </div>
            </div>

            <!-- Other Possibilities -->
            <div v-if="otherResults.length > 0" class="bg-white rounded-xl border border-[#bcc9c6]/30 overflow-hidden shadow-sm print:hidden">
              <div class="px-6 py-4 border-b border-[#bcc9c6]/20 bg-[#f8f9ff] flex items-center gap-2">
                <ListCollapse class="text-[#6d7a77] w-5 h-5" />
                <div>
                  <p class="font-bold text-sm text-[#0b1c30]">Kemungkinan Lainnya</p>
                  <p class="text-[11px] text-[#6d7a77]">Penyakit lain yang memiliki kemiripan gejala</p>
                </div>
              </div>
              <div class="divide-y divide-[#bcc9c6]/20">
                <div v-for="(item, idx) in otherResults" :key="item.penyakit_id" 
                     class="flex items-center gap-4 px-6 py-4 hover:bg-[#f8f9ff] transition-colors">
                  <div class="w-8 h-8 rounded-xl flex items-center justify-center font-bold text-xs bg-[#e5eeff] text-[#3d4947]">
                    {{ idx + 2 }}
                  </div>
                  <div class="flex-1 min-w-0">
                    <p class="font-semibold text-sm text-[#0b1c30] truncate">{{ item.nama_penyakit }}</p>
                    <div class="flex items-center gap-2 mt-1.5">
                      <div class="flex-1 h-1.5 rounded-full overflow-hidden max-w-[120px] bg-[#e5eeff]">
                        <div class="h-full rounded-full bg-[#6d7a77]" :style="{ width: `${Math.min(item.persentase, 100)}%` }"></div>
                      </div>
                      <span class="text-[11px] font-semibold text-[#6d7a77]">{{ item.persentase.toFixed(2) }}%</span>
                    </div>
                  </div>
                  <span class="inline-flex px-2.5 py-0.5 rounded-full text-[10px] font-bold border bg-[#eff4ff] border-[#bcc9c6]/50 text-[#3d4947]">
                    {{ item.status }}
                  </span>
                </div>
              </div>
            </div>

            <!-- Action Area -->
            <div class="flex flex-col sm:flex-row justify-center gap-4 mt-8 border-t border-[#bcc9c6]/30 pt-6 print:hidden">
              <button @click="resetDiagnosa" 
                      class="bg-[#00685f] text-white hover:bg-[#005049] text-xs font-semibold px-6 py-3 rounded-lg shadow-sm transition-colors flex items-center justify-center gap-2 active:scale-95 cursor-pointer">
                <RotateCcw class="w-4 h-4 text-white" />
                <span>Konsultasi Ulang</span>
              </button>
              <button @click="printResult" 
                      class="bg-white text-[#00685f] border border-[#00685f] hover:bg-[#e5eeff] text-xs font-semibold px-6 py-3 rounded-lg transition-colors flex items-center justify-center gap-2 active:scale-95 cursor-pointer">
                <Printer class="w-4 h-4 text-[#00685f]" />
                <span>Cetak Hasil</span>
              </button>
            </div>

          </div>
        </div>

      </Transition>
    </div>
  </UserLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth.store'
import { useGejalaStore } from '@/stores/gejala.store'
import { useDiagnosaStore } from '@/stores/diagnosa.store'
import { useRiwayatStore } from '@/stores/riwayat.store'
import UserLayout from '@/layouts/UserLayout.vue'
import AppBreadcrumb from '@/components/common/AppBreadcrumb.vue'
import PageHeader from '@/components/common/PageHeader.vue'
import FullScreenLoader from '@/components/common/FullScreenLoader.vue'
import { 
  ArrowRight, Stethoscope, FileText, HeartPulse, ListCollapse, 
  RotateCcw, Printer, Thermometer, Wind, Ear, Siren, Droplets, Info
} from 'lucide-vue-next'


const authStore = useAuthStore()
const gejalaStore = useGejalaStore()
const diagnosaStore = useDiagnosaStore()
const riwayatStore = useRiwayatStore()

const userId = computed(() => authStore.currentUser?.id || null)

const gejalaList = computed(() => gejalaStore.gejalaList)
const loadingGejala = computed(() => gejalaStore.loading)
const isLoading = computed(() => diagnosaStore.loading)
const diagnosaResult = computed(() => diagnosaStore.result)

const selectedGejala = ref([])
const fetchError     = ref(null)
const diagnosaError  = ref(null)
const showDetailPerhitungan = ref(false)

const topResult    = computed(() => diagnosaResult.value?.hasil?.[0] || null)
const otherResults = computed(() => diagnosaResult.value?.hasil?.slice(1) || [])

const solutionsList = computed(() => {
  if (!topResult.value?.solusi) return []
  return topResult.value.solusi
    .split('\n')
    .map(s => s.trim())
    .filter(s => s.length > 0)
    .map(s => s.replace(/^[-*\u2022]\s*/, '')) // remove list bullet prefix
})

const getSymptomDescription = (name) => {
  const map = {
    'Sakit Tenggorokan': 'Rasa sakit, gatal, atau iritasi pada tenggorokan yang biasanya memburuk saat menelan.',
    'Telinga Berdengung': 'Suara berdengung, berdesir, atau berdencing di dalam telinga (Tinnitus).',
    'Demam': 'Kenaikan suhu tubuh yang dikaitkan dengan proses infeksi atau radang.',
    'Hidung Tersumbat': 'Kesulitan bernapas melalui hidung akibat penyumbatan mukosa.',
    'Nyeri Menelan': 'Discomfort atau rasa sakit tajam saat melakukan gerakan menelan.',
  }
  return map[name] || 'Gejala klinis THT. Pilih jika Anda merasakan kondisi ini untuk membantu diagnosis.'
}

const getSymptomIconComponent = (name) => {
  const nameLower = name.toLowerCase()
  if (nameLower.includes('tenggorokan')) return Siren
  if (nameLower.includes('dengung') || nameLower.includes('telinga') || nameLower.includes('dengar')) return Ear
  if (nameLower.includes('demam') || nameLower.includes('panas') || nameLower.includes('suhu')) return Thermometer
  if (nameLower.includes('sumbat') || nameLower.includes('hidung') || nameLower.includes('napas') || nameLower.includes('pilek')) return Wind
  if (nameLower.includes('menelan') || nameLower.includes('tenggorok') || nameLower.includes('nyeri')) return Droplets
  return Info
}

const fetchGejala = async () => {
  fetchError.value = null
  try {
    await gejalaStore.fetchGejala()
  } catch (err) {
    fetchError.value = err.message || 'Gagal terhubung ke server.'
  }
}

const handleDiagnosa = async () => {
  if (selectedGejala.value.length === 0) {
    diagnosaError.value = 'Silakan pilih setidaknya satu gejala.'
    return
  }
  diagnosaError.value = null
  try {
    await diagnosaStore.runDiagnosa(userId.value, selectedGejala.value)
    // Refresh riwayat store agar dashboard & halaman riwayat langsung terupdate
    if (userId.value) {
      riwayatStore.fetchByUser(userId.value).catch(() => {}) // non-blocking
    }
    window.scrollTo({ top: 0, behavior: 'smooth' })
  } catch (err) {
    diagnosaError.value = err.message || 'Terjadi kesalahan saat menjalankan diagnosa.'
  }
}

const resetDiagnosa = () => {
  diagnosaStore.$reset()
  diagnosaError.value  = null
  selectedGejala.value = []
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

const printResult = () => {
  const user      = authStore.currentUser
  const patientName = user?.name  || 'Pasien'
  const patientEmail = user?.email || '-'
  const result    = topResult.value
  const solutions = solutionsList.value
  const others    = otherResults.value

  const now = new Date()
  const printDate = now.toLocaleDateString('id-ID', {
    weekday: 'long', day: 'numeric', month: 'long', year: 'numeric'
  })
  const printTime = now.toLocaleTimeString('id-ID', { hour: '2-digit', minute: '2-digit' })

  // Badge warna status
  const statusColor = result.persentase >= 80
    ? '#15803d' : result.persentase >= 50 ? '#b45309' : '#374151'
  const statusBg    = result.persentase >= 80
    ? '#dcfce7' : result.persentase >= 50 ? '#fef3c7' : '#f3f4f6'

  // Daftar saran medis
  const solutionsHtml = solutions.length > 0
    ? solutions.map(s => `<li>${s}</li>`).join('')
    : '<li><em>Konsultasikan dengan dokter spesialis THT untuk rekomendasi penanganan.</em></li>'

  // Kemungkinan lainnya
  const othersHtml = others.length > 0 ? `
    <div class="section">
      <div class="section-title">📋 Kemungkinan Diagnosis Lainnya</div>
      <table class="other-table">
        <thead>
          <tr>
            <th>#</th>
            <th>Nama Penyakit</th>
            <th>Probabilitas</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          ${others.map((o, i) => `
            <tr>
              <td style="text-align:center;color:#6b7280">${i + 2}</td>
              <td>${o.nama_penyakit}</td>
              <td style="text-align:center;font-weight:600">${o.persentase.toFixed(2)}%</td>
              <td style="text-align:center">
                <span class="badge-other">${o.status}</span>
              </td>
            </tr>`).join('')}
        </tbody>
      </table>
    </div>` : ''

  const html = `<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8" />
  <title>Hasil Pemeriksaan — ${patientName}</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      font-family: 'Times New Roman', Times, serif;
      font-size: 12pt;
      color: #1a1a1a;
      background: #fff;
      padding: 32px 48px;
      max-width: 800px;
      margin: 0 auto;
    }

    /* ── KOP SURAT ── */
    .letterhead {
      display: flex;
      align-items: center;
      gap: 20px;
      border-bottom: 3px solid #004d40;
      padding-bottom: 16px;
      margin-bottom: 4px;
    }
    .letterhead-logo {
      width: 60px; height: 60px;
      border-radius: 50%;
      background: #004d40;
      display: flex; align-items: center; justify-content: center;
      color: #fff;
      font-size: 22pt;
      font-weight: bold;
      flex-shrink: 0;
      font-family: Arial, sans-serif;
    }
    .letterhead-info h1 {
      font-size: 16pt;
      font-weight: bold;
      color: #004d40;
      letter-spacing: 0.5px;
      font-family: Arial, sans-serif;
    }
    .letterhead-info p {
      font-size: 9pt;
      color: #555;
      margin-top: 2px;
    }
    .letterhead-right {
      margin-left: auto;
      text-align: right;
      font-size: 9pt;
      color: #555;
    }
    .subtitle-bar {
      background: #004d40;
      color: #fff;
      text-align: center;
      font-family: Arial, sans-serif;
      font-size: 11pt;
      font-weight: bold;
      letter-spacing: 1px;
      padding: 5px 0;
      margin-bottom: 20px;
    }

    /* ── INFO PASIEN ── */
    .patient-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 6px 32px;
      background: #f8fffe;
      border: 1px solid #b2dfdb;
      border-radius: 6px;
      padding: 14px 18px;
      margin-bottom: 20px;
      font-size: 10.5pt;
    }
    .patient-grid .row { display: contents; }
    .patient-grid .label { color: #666; font-style: italic; }
    .patient-grid .value { font-weight: bold; color: #1a1a1a; }

    /* ── SECTION ── */
    .section { margin-bottom: 18px; }
    .section-title {
      font-family: Arial, sans-serif;
      font-size: 11pt;
      font-weight: bold;
      color: #004d40;
      border-left: 4px solid #004d40;
      padding-left: 8px;
      margin-bottom: 10px;
    }

    /* ── HASIL UTAMA ── */
    .result-box {
      border: 2px solid #004d40;
      border-radius: 8px;
      overflow: hidden;
      margin-bottom: 20px;
    }
    .result-header {
      background: #004d40;
      color: #fff;
      padding: 10px 16px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .result-header .disease-name {
      font-size: 15pt;
      font-weight: bold;
      font-family: Arial, sans-serif;
    }
    .result-header .no-label {
      font-size: 9pt;
      opacity: 0.8;
    }
    .result-body { padding: 14px 16px; }

    /* progress bar */
    .prob-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 6px;
    }
    .prob-label { font-size: 9pt; color: #555; }
    .prob-value {
      font-size: 14pt;
      font-weight: bold;
      color: #004d40;
    }
    .badge {
      display: inline-block;
      padding: 2px 10px;
      border-radius: 12px;
      font-size: 8.5pt;
      font-weight: bold;
      font-family: Arial, sans-serif;
      background: ${statusBg};
      color: ${statusColor};
    }
    .progress-track {
      height: 8px;
      background: #e0f2f1;
      border-radius: 4px;
      margin-bottom: 14px;
      overflow: hidden;
    }
    .progress-fill {
      height: 100%;
      border-radius: 4px;
      background: #004d40;
      width: ${Math.min(result.persentase, 100)}%;
    }
    .desc-text { font-size: 10.5pt; line-height: 1.7; color: #333; margin-bottom: 12px; }
    .solutions { padding-left: 18px; }
    .solutions li { font-size: 10.5pt; line-height: 1.8; color: #333; }

    /* ── TABEL KEMUNGKINAN LAIN ── */
    .other-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 10pt;
    }
    .other-table th {
      background: #e0f2f1;
      color: #004d40;
      padding: 7px 10px;
      text-align: left;
      font-family: Arial, sans-serif;
      font-size: 9pt;
      border: 1px solid #b2dfdb;
    }
    .other-table td {
      padding: 7px 10px;
      border: 1px solid #e5e7eb;
      vertical-align: middle;
    }
    .other-table tr:nth-child(even) td { background: #f9fffe; }
    .badge-other {
      display: inline-block;
      background: #f3f4f6;
      color: #374151;
      border-radius: 10px;
      padding: 1px 8px;
      font-size: 8.5pt;
      font-weight: bold;
    }

    /* ── DISCLAIMER ── */
    .disclaimer {
      border: 1px solid #f59e0b;
      background: #fffbeb;
      border-radius: 6px;
      padding: 12px 16px;
      margin-top: 20px;
      font-size: 9pt;
      color: #78350f;
      line-height: 1.6;
    }
    .disclaimer strong { color: #92400e; }

    /* ── TANDA TANGAN ── */
    .signature-area {
      margin-top: 30px;
      display: flex;
      justify-content: flex-end;
    }
    .signature-box {
      text-align: center;
      font-size: 10pt;
    }
    .signature-box .sig-name {
      font-weight: bold;
      margin-top: 48px;
      border-top: 1px solid #333;
      padding-top: 4px;
    }
    .signature-box .sig-title { font-size: 9pt; color: #555; }

    /* ── FOOTER ── */
    .page-footer {
      margin-top: 28px;
      border-top: 1px solid #b2dfdb;
      padding-top: 8px;
      display: flex;
      justify-content: space-between;
      font-size: 8pt;
      color: #999;
    }

    @media print {
      body { padding: 20px 32px; }
      button { display: none !important; }
    }
  </style>
</head>
<body>

  <!-- KOP SURAT -->
  <div class="letterhead">
    <div class="letterhead-logo">RS</div>
    <div class="letterhead-info">
      <h1>RS JASA KARTINI</h1>
      <p>Jl. Kesehatan No. 1, Tasikmalaya, Jawa Barat</p>
      <p>Telp: (0265) 123-456 &nbsp;|&nbsp; Email: info@rskartini.id</p>
    </div>
    <div class="letterhead-right">
      <p><strong>Poliklinik THT</strong></p>
      <p>Spesialis Telinga Hidung Tenggorokan</p>
    </div>
  </div>
  <div class="subtitle-bar">SURAT HASIL SKRINING KESEHATAN THT</div>

  <!-- INFO PASIEN -->
  <div class="patient-grid">
    <span class="label">Nama Pasien</span>
    <span class="value">${patientName}</span>
    <span class="label">Email</span>
    <span class="value">${patientEmail}</span>
    <span class="label">Tanggal Cetak</span>
    <span class="value">${printDate}, ${printTime} WIB</span>
    <span class="label">No. Dokumen</span>
    <span class="value">SP-THT-${now.getFullYear()}${String(now.getMonth()+1).padStart(2,'0')}${String(now.getDate()).padStart(2,'0')}-${Math.floor(Math.random()*9000+1000)}</span>
  </div>

  <!-- HASIL DIAGNOSIS UTAMA -->
  <div class="result-box">
    <div class="result-header">
      <div>
        <div class="no-label">Diagnosis Utama</div>
        <div class="disease-name">🩺 ${result.nama_penyakit}</div>
      </div>
      <span class="badge">${result.status}</span>
    </div>
    <div class="result-body">
      <div class="prob-row">
        <span class="prob-label">Tingkat Keyakinan Sistem</span>
        <span class="prob-value">${result.persentase.toFixed(2)}%</span>
      </div>
      <div class="progress-track"><div class="progress-fill"></div></div>

      <div class="section-title">📄 Deskripsi Penyakit</div>
      <p class="desc-text">${result.deskripsi || 'Belum tersedia deskripsi untuk penyakit ini.'}</p>

      <div class="section-title">💊 Saran Medis & Penanganan</div>
      <ul class="solutions">${solutionsHtml}</ul>
    </div>
  </div>

  <!-- KEMUNGKINAN LAIN -->
  ${othersHtml}

  <!-- DISCLAIMER -->
  <div class="disclaimer">
    ⚠️ <strong>Perhatian:</strong>
    Dokumen ini merupakan hasil <strong>skrining awal berbasis sistem pakar</strong> dan bersifat sebagai informasi pendukung.
    Hasil ini <strong>tidak dapat menggantikan</strong> pemeriksaan fisik, diagnosis klinis, atau rekomendasi langsung dari dokter spesialis THT.
    Segera kunjungi fasilitas kesehatan terdekat apabila gejala berlanjut atau memburuk.
  </div>

  <!-- TANDA TANGAN -->
  <div class="signature-area">
    <div class="signature-box">
      <p>${printDate}</p>
      <div class="sig-name">Sistem Pakar THT</div>
      <div class="sig-title">RS Jasa Kartini — Kelompok 2</div>
    </div>
  </div>

  <!-- FOOTER -->
  <div class="page-footer">
    <span>Sistem Pakar THT v1.0 — RS Jasa Kartini</span>
    <span>Dicetak: ${printDate} ${printTime} WIB</span>
  </div>

  <script>
    window.onload = () => window.print();
  <\/script>
</body>
</html>`

  const win = window.open('', '_blank', 'width=860,height=900,scrollbars=yes')
  win.document.write(html)
  win.document.close()
}

onMounted(fetchGejala)
</script>

<style scoped>
.page-slide-enter-active { transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1); }
.page-slide-leave-active { transition: all 0.2s ease-in; }
.page-slide-enter-from   { opacity: 0; transform: translateY(16px); }
.page-slide-leave-to     { opacity: 0; transform: translateY(-8px); }

.slide-down-enter-active { transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1); }
.slide-down-leave-active { transition: all 0.2s ease-in; }
.slide-down-enter-from   { opacity: 0; transform: translateY(-8px); }
.slide-down-leave-to     { opacity: 0; transform: translateY(-4px); }
</style>
