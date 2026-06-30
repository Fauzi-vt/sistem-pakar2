<template>
  <UserLayout>
    <AppBreadcrumb :items="[{ label: 'Dashboard', to: '/user/dashboard' }, { label: 'Konsultasi' }]" />
    
    <FullScreenLoader 
      :isVisible="isLoading" 
      title="Memproses Diagnosa" 
      message="Sistem sedang menghitung probabilitas berdasarkan gejala Anda..." 
    />

    <!-- Main Content -->
    <div class="max-w-3xl mx-auto py-4">
      <Transition name="page-slide" mode="out-in">
        
        <!-- ════ STEP 1 — Symptom Selection ════ -->
        <div v-if="!diagnosaResult" key="step1">
          <PageHeader 
            title="Checklist Gejala" 
            description="Pilih gejala yang Anda alami untuk memulai asesmen THT awal menggunakan probabilitas Bayes." 
          />

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
            
            <!-- Selected symptoms count badge -->
            <Transition name="slide-down">
              <div v-if="selectedGejala.length > 0" class="flex items-center gap-2.5 px-4 py-2.5 rounded-lg border text-xs font-semibold bg-[#e0f2f1] border-[#00685f]/20 text-[#005049]">
                <div class="w-6 h-6 rounded-md flex items-center justify-center text-white bg-[#00685f]">
                  {{ selectedGejala.length }}
                </div>
                <span>gejala dipilih — siap untuk memproses diagnosa</span>
              </div>
            </Transition>

            <div class="space-y-3">
              <!-- Checklist Items -->
              <label v-for="item in gejalaList" :key="item.id"
                     class="flex items-start p-4 rounded-lg hover:bg-[#eff4ff] transition-colors cursor-pointer border border-transparent hover:border-[#bcc9c6]/30 group">
                <div class="flex items-center h-6">
                  <input class="w-5 h-5 text-[#00685f] border-[#bcc9c6] rounded focus:ring-[#00685f]/50 focus:ring-offset-0 bg-white cursor-pointer" 
                         type="checkbox"
                         :value="item.id"
                         v-model="selectedGejala"/>
                </div>
                <div class="ml-4 flex-1">
                  <span class="text-base font-semibold text-[#0b1c30] block mb-1 group-hover:text-[#00685f] transition-colors">
                    {{ item.nama }}
                  </span>
                  <span class="text-xs text-[#3d4947]">
                    {{ getSymptomDescription(item.nama) }} ({{ item.kode }})
                  </span>
                </div>
                <span class="text-[#6d7a77] group-hover:text-[#00685f] ml-2 opacity-0 group-hover:opacity-100 transition-opacity">
                  <component :is="getSymptomIconComponent(item.nama)" class="w-5 h-5" />
                </span>
              </label>
            </div>

            <!-- Error message on submit -->
            <Transition name="slide-down">
              <div v-if="diagnosaError" class="p-3 text-xs text-[#93000a] bg-[#ffdad6] border border-[#ba1a1a]/20 rounded-lg">
                {{ diagnosaError }}
              </div>
            </Transition>

            <div class="flex justify-end border-t border-[#bcc9c6]/30 pt-6 mt-6">
              <button @click="handleDiagnosa" 
                      :disabled="selectedGejala.length === 0 || isLoading"
                      class="bg-[#00685f] hover:bg-[#006a61] text-white text-xs font-semibold py-3 px-6 rounded-lg shadow-sm transition-all flex items-center justify-center min-w-[160px] min-h-[44px] active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer" 
                      type="button">
                <span v-if="isLoading" class="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin mr-2"></span>
                <span>Proses Diagnosa</span>
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
                      <span class="text-xs font-semibold text-[#3d4947]">Tingkat Keyakinan (Teorema Bayes)</span>
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

                    <!-- Transparansi Perhitungan (Metode Bayes) -->
                    <div class="mt-6 pt-6 border-t border-[#bcc9c6]/30 print:hidden" v-if="topResult.detail && topResult.detail.total_h !== undefined">
                      <button @click="showDetailPerhitungan = !showDetailPerhitungan"
                              class="w-full flex items-center justify-between p-4 bg-[#f8f9ff] hover:bg-[#eff4ff] rounded-xl border border-[#bcc9c6]/30 transition-colors cursor-pointer group">
                        <div class="flex items-center gap-3">
                          <div class="w-8 h-8 rounded-lg bg-[#e5eeff] flex items-center justify-center text-[#006387] group-hover:bg-[#006387] group-hover:text-white transition-colors">
                            <Calculator class="w-4 h-4" />
                          </div>
                          <div class="text-left">
                            <h4 class="text-sm font-bold text-[#0b1c30]">Transparansi Algoritma (Teorema Bayes)</h4>
                            <p class="text-[11px] text-[#6d7a77]">Lihat rincian kalkulasi matematika untuk hasil ini</p>
                          </div>
                        </div>
                        <ChevronDown v-if="!showDetailPerhitungan" class="w-5 h-5 text-[#6d7a77] group-hover:text-[#006387]" />
                        <ChevronUp v-else class="w-5 h-5 text-[#006387]" />
                      </button>

                      <Transition name="slide-down">
                        <div v-if="showDetailPerhitungan" class="mt-3 bg-white border border-[#bcc9c6]/30 rounded-xl overflow-hidden shadow-sm">
                          <div class="p-4 bg-[#f4f7f6] border-b border-[#bcc9c6]/30">
                            <p class="text-xs font-semibold text-[#00685f]">
                              <span class="font-bold">Metode Penjumlahan (Sigma):</span>
                            </p>
                          </div>
                          
                          <div class="overflow-x-auto">
                            <table class="w-full text-left text-xs">
                              <thead class="bg-[#f8f9ff] text-[#3d4947]">
                                <tr>
                                  <th class="px-4 py-3 font-semibold border-b border-[#bcc9c6]/20">Gejala Cocok (E)</th>
                                  <th class="px-4 py-3 font-semibold border-b border-[#bcc9c6]/20">Likelihood P(E|H)</th>
                                  <th class="px-4 py-3 font-semibold border-b border-[#bcc9c6]/20">Prior P(H)</th>
                                  <th class="px-4 py-3 font-semibold border-b border-[#bcc9c6]/20">Posterior P(H|E)</th>
                                </tr>
                              </thead>
                              <tbody class="divide-y divide-[#bcc9c6]/10">
                                <tr v-for="(gejalaId, idx) in topResult.gejala_cocok" :key="idx" class="hover:bg-[#f8f9ff]/50 transition-colors">
                                  <td class="px-4 py-3 font-medium text-[#0b1c30]">Gejala ID: {{ gejalaId }}</td>
                                  <td class="px-4 py-3 text-[#3d4947]">{{ topResult.detail.nilai_gejala[idx].toFixed(4) }}</td>
                                  <td class="px-4 py-3 text-[#3d4947]">{{ topResult.detail.prior_list[idx].toFixed(4) }}</td>
                                  <td class="px-4 py-3 text-[#00685f] font-semibold">{{ topResult.detail.posterior_list[idx].toFixed(4) }}</td>
                                </tr>
                              </tbody>
                            </table>
                          </div>
                          
                          <div class="p-4 bg-[#f8f9ff] border-t border-[#bcc9c6]/20 space-y-2 text-xs">
                            <div class="flex justify-between items-center">
                              <span class="text-[#6d7a77]">Total Semesta (ΣH)</span>
                              <span class="font-mono font-semibold text-[#0b1c30]">{{ topResult.detail.total_h.toFixed(4) }}</span>
                            </div>
                            <div class="flex justify-between items-center">
                              <span class="text-[#6d7a77]">Probabilitas Evidence (PE)</span>
                              <span class="font-mono font-semibold text-[#0b1c30]">{{ topResult.detail.probabilitas_evidence.toFixed(4) }}</span>
                            </div>
                            <div class="flex justify-between items-center pt-2 border-t border-[#bcc9c6]/20 mt-2">
                              <span class="font-bold text-[#00685f]">Hasil Akhir Diagnosis</span>
                              <span class="font-mono font-bold text-[#00685f]">{{ (topResult.detail.nilai_bayes * 100).toFixed(4) }}%</span>
                            </div>
                          </div>
                        </div>
                      </Transition>
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
  RotateCcw, Printer, Thermometer, Wind, Ear, Siren, Droplets, Info,
  Calculator, ChevronDown, ChevronUp
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
  window.print()
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
