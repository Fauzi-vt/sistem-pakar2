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
          <!-- 1. Ringkasan Hasil (paling atas) -->
          <header class="mb-6 text-center md:text-left bg-gradient-to-r from-[#00685f] to-[#004d40] text-white p-8 rounded-2xl shadow-lg relative overflow-hidden">
            <div class="absolute top-0 right-0 opacity-10">
              <Stethoscope class="w-48 h-48 -mt-8 -mr-8" />
            </div>
            <div class="relative z-10">
              <p class="text-sm font-semibold text-[#a7f3d0] mb-1 tracking-wider uppercase">Hasil Diagnosis</p>
              <h1 class="text-4xl font-extrabold mb-4 flex items-center gap-3">
                <span v-if="topResult">{{ topResult.nama_penyakit }}</span>
                <span v-else>Tidak Ditemukan</span>
              </h1>
              
              <div v-if="topResult" class="flex flex-col sm:flex-row sm:items-center gap-4 sm:gap-8">
                <div>
                  <p class="text-sm text-[#a7f3d0] mb-1">Tingkat Probabilitas</p>
                  <div class="flex items-baseline gap-2">
                    <span class="text-3xl font-bold">{{ topResult.persentase.toFixed(2) }}%</span>
                    <span class="text-xs font-bold px-2.5 py-1 rounded-full bg-white/20 backdrop-blur-sm border border-white/30">
                      {{ topResult.status }}
                    </span>
                  </div>
                </div>
                <div class="hidden sm:block w-px h-12 bg-white/20"></div>
                <div class="flex-1 max-w-md">
                  <p class="text-sm text-white/90">
                    <strong>Status:</strong> Kemungkinan besar gejala yang Anda alami mengarah pada <strong>{{ topResult.nama_penyakit }}</strong>.
                  </p>
                </div>
              </div>
            </div>
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
            
            <!-- 2. Gejala yang dipilih pengguna -->
            <div class="bg-white rounded-xl border border-[#bcc9c6]/30 p-6 shadow-sm">
              <h3 class="text-base font-bold text-[#0b1c30] mb-4 flex items-center gap-2">
                <CheckSquare class="text-[#00685f] w-5 h-5" />
                <span>Gejala yang Anda pilih</span>
              </h3>
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <div v-for="gejala in selectedGejalaDetails" :key="gejala.id" class="flex items-center gap-2 text-sm text-[#3d4947]">
                  <Check class="w-4 h-4 text-[#00685f] shrink-0" />
                  <span>{{ gejala.nama }}</span>
                </div>
              </div>
            </div>

            <!-- 10. Mengapa sistem memberikan hasil ini? (Explainability) -->
            <div class="bg-gradient-to-br from-[#f8f9ff] to-[#eef2ff] rounded-xl border border-[#d0d7ff] p-6 shadow-sm">
              <h3 class="text-base font-bold text-[#1e3a8a] mb-2 flex items-center gap-2">
                <BrainCircuit class="text-[#3b82f6] w-5 h-5" />
                <span>Mengapa sistem memberikan hasil ini?</span>
              </h3>
              <p class="text-sm text-[#475569] mb-4">
                Sistem menganalisis berdasarkan Teorema Bayes. Gejala yang paling berpengaruh terhadap hasil <strong>{{ topResult.nama_penyakit }}</strong>:
              </p>
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 mb-4">
                <div v-for="gejala in selectedGejalaDetails" :key="'explain-'+gejala.id" class="flex items-center gap-2 text-sm text-[#1e293b] bg-white px-3 py-2 rounded-lg border border-[#e2e8f0]">
                  <CheckCircle2 class="w-4 h-4 text-[#10b981] shrink-0" />
                  <span class="font-medium">{{ gejala.nama }}</span>
                </div>
              </div>
              <p class="text-xs text-[#64748b] italic">
                Gejala-gejala tersebut memiliki probabilitas tinggi terhadap penyakit {{ topResult.nama_penyakit }} berdasarkan basis pengetahuan sistem.
              </p>
            </div>

            <!-- 3. Hasil seluruh penyakit -->
            <div class="bg-white rounded-xl border border-[#bcc9c6]/30 p-6 shadow-sm">
              <h3 class="text-base font-bold text-[#0b1c30] mb-4 flex items-center gap-2">
                <List class="text-[#00685f] w-5 h-5" />
                <span>Hasil Analisis Seluruh Penyakit</span>
              </h3>
              <div class="overflow-x-auto">
                <table class="w-full text-sm text-left">
                  <thead class="text-xs text-[#6d7a77] uppercase bg-[#f8f9ff] border-b border-[#bcc9c6]/30">
                    <tr>
                      <th class="px-4 py-3 font-semibold">Penyakit</th>
                      <th class="px-4 py-3 font-semibold w-1/2">Probabilitas</th>
                      <th class="px-4 py-3 font-semibold text-right">Nilai</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="(item, idx) in diagnosaResult.hasil" :key="item.penyakit_id" class="border-b border-[#bcc9c6]/10 last:border-0 hover:bg-[#f8f9ff]/50 transition-colors">
                      <td class="px-4 py-3 font-medium" :class="idx === 0 ? 'text-[#00685f] font-bold' : 'text-[#3d4947]'">
                        {{ item.nama_penyakit }}
                        <span v-if="idx === 0" class="ml-2 inline-flex px-2 py-0.5 rounded text-[9px] font-bold bg-[#dcfce7] text-[#15803d]">UTAMA</span>
                      </td>
                      <td class="px-4 py-3">
                        <div class="flex items-center gap-2 w-full">
                          <div class="flex-1 h-2 rounded-full bg-[#e5eeff] overflow-hidden">
                            <div class="h-full rounded-full transition-all duration-1000" 
                                 :class="idx === 0 ? 'bg-[#00685f]' : 'bg-[#94a3b8]'"
                                 :style="{ width: `${Math.min(item.persentase, 100)}%` }"></div>
                          </div>
                        </div>
                      </td>
                      <td class="px-4 py-3 text-right font-semibold" :class="idx === 0 ? 'text-[#00685f]' : 'text-[#64748b]'">
                        {{ item.persentase.toFixed(2) }}%
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>

            <!-- Detail Penyakit Utama -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              
              <!-- 4. Deskripsi -->
              <div class="bg-white rounded-xl border border-[#bcc9c6]/30 p-6 shadow-sm h-full">
                <h3 class="text-base font-bold text-[#0b1c30] mb-3 flex items-center gap-2">
                  <FileText class="text-[#006387] w-5 h-5" />
                  <span>Deskripsi Penyakit</span>
                </h3>
                <p class="text-sm leading-relaxed text-[#475569]">
                  {{ topResult.deskripsi || 'Belum ada penjelasan deskriptif yang tersedia untuk penyakit ini.' }}
                </p>
              </div>

              <!-- 5. Penyebab (Static/Placeholder) -->
              <div class="bg-white rounded-xl border border-[#bcc9c6]/30 p-6 shadow-sm h-full">
                <h3 class="text-base font-bold text-[#0b1c30] mb-3 flex items-center gap-2">
                  <Microscope class="text-[#ea580c] w-5 h-5" />
                  <span>Penyebab Umum</span>
                </h3>
                <ul class="text-sm leading-relaxed text-[#475569] space-y-2">
                  <li class="flex items-start gap-2">
                    <span class="w-1.5 h-1.5 rounded-full bg-[#ea580c] mt-1.5 shrink-0"></span>
                    <span>Infeksi virus atau bakteri.</span>
                  </li>
                  <li class="flex items-start gap-2">
                    <span class="w-1.5 h-1.5 rounded-full bg-[#ea580c] mt-1.5 shrink-0"></span>
                    <span>Daya tahan tubuh yang sedang menurun.</span>
                  </li>
                  <li class="flex items-start gap-2">
                    <span class="w-1.5 h-1.5 rounded-full bg-[#ea580c] mt-1.5 shrink-0"></span>
                    <span>Paparan dari penderita infeksi (penularan).</span>
                  </li>
                  <li class="flex items-start gap-2">
                    <span class="w-1.5 h-1.5 rounded-full bg-[#ea580c] mt-1.5 shrink-0"></span>
                    <span>Faktor lingkungan atau alergen tertentu.</span>
                  </li>
                </ul>
              </div>

              <!-- 6. Saran Penanganan -->
              <div class="bg-white rounded-xl border border-[#bcc9c6]/30 p-6 shadow-sm h-full">
                <h3 class="text-base font-bold text-[#0b1c30] mb-3 flex items-center gap-2">
                  <HeartPulse class="text-[#10b981] w-5 h-5" />
                  <span>Saran Penanganan Awal</span>
                </h3>
                <ul v-if="solutionsList.length > 0" class="text-sm leading-relaxed text-[#475569] space-y-2">
                  <li v-for="sol in solutionsList" :key="sol" class="flex items-start gap-2">
                    <span class="w-1.5 h-1.5 rounded-full bg-[#10b981] mt-1.5 shrink-0"></span>
                    <span>{{ sol }}</span>
                  </li>
                </ul>
                <p v-else class="text-sm text-[#6d7a77] italic">Tidak ada saran medis spesifik, perbanyak istirahat.</p>
              </div>

              <!-- 7. Kapan harus ke dokter -->
              <div class="bg-[#fff1f2] rounded-xl border border-[#fecdd3] p-6 shadow-sm h-full">
                <h3 class="text-base font-bold text-[#be123c] mb-3 flex items-center gap-2">
                  <AlertTriangle class="text-[#e11d48] w-5 h-5" />
                  <span>Segera ke Dokter Apabila:</span>
                </h3>
                <ul class="text-sm leading-relaxed text-[#9f1239] space-y-2">
                  <li class="flex items-start gap-2">
                    <span class="w-1.5 h-1.5 rounded-full bg-[#e11d48] mt-1.5 shrink-0"></span>
                    <span>Demam tinggi lebih dari 3 hari.</span>
                  </li>
                  <li class="flex items-start gap-2">
                    <span class="w-1.5 h-1.5 rounded-full bg-[#e11d48] mt-1.5 shrink-0"></span>
                    <span>Sulit bernapas atau sesak napas.</span>
                  </li>
                  <li class="flex items-start gap-2">
                    <span class="w-1.5 h-1.5 rounded-full bg-[#e11d48] mt-1.5 shrink-0"></span>
                    <span>Tidak dapat menelan makanan atau minuman sama sekali.</span>
                  </li>
                  <li class="flex items-start gap-2">
                    <span class="w-1.5 h-1.5 rounded-full bg-[#e11d48] mt-1.5 shrink-0"></span>
                    <span>Nyeri yang semakin berat dan tidak tertahankan.</span>
                  </li>
                </ul>
              </div>
            </div>

            <!-- 8. Disclaimer -->
            <div class="bg-[#fffbeb] border border-[#fcd34d] rounded-xl p-5 shadow-sm mt-4">
              <div class="flex gap-3">
                <Info class="w-6 h-6 text-[#d97706] shrink-0" />
                <div class="text-sm text-[#92400e]">
                  <p class="font-bold mb-1">Catatan Penting</p>
                  <p>Hasil diagnosis ini merupakan estimasi awal berdasarkan gejala yang Anda pilih menggunakan metode <strong>Teorema Bayes</strong>.</p>
                  <p class="mt-1 font-semibold">Hasil ini BUKAN pengganti diagnosis medis resmi maupun pemeriksaan langsung oleh dokter spesialis.</p>
                </div>
              </div>
            </div>

            <!-- 9. Tombol Aksi -->
            <div class="flex flex-col sm:flex-row justify-center gap-4 mt-8 border-t border-[#bcc9c6]/30 pt-6 print:hidden">
              <button @click="resetDiagnosa" 
                      class="bg-white text-[#00685f] border-2 border-[#00685f] hover:bg-[#f0fdfa] text-xs font-bold px-6 py-3 rounded-lg transition-colors flex items-center justify-center gap-2 cursor-pointer">
                <RotateCcw class="w-4 h-4" />
                <span>Diagnosa Ulang</span>
              </button>
              <button @click="saveRiwayatManual" 
                      class="bg-[#00685f] text-white hover:bg-[#005049] text-xs font-bold px-6 py-3 rounded-lg shadow-sm transition-colors flex items-center justify-center gap-2 cursor-pointer">
                <Save class="w-4 h-4" />
                <span>Simpan Riwayat</span>
              </button>
              <button @click="printResult" 
                      class="bg-[#1e293b] text-white hover:bg-[#0f172a] text-xs font-bold px-6 py-3 rounded-lg shadow-sm transition-colors flex items-center justify-center gap-2 cursor-pointer">
                <Printer class="w-4 h-4" />
                <span>Cetak PDF</span>
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
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth.store'
import { useGejalaStore } from '@/stores/gejala.store'
import { useDiagnosaStore } from '@/stores/diagnosa.store'
import { useRiwayatStore } from '@/stores/riwayat.store'
import UserLayout from '@/layouts/UserLayout.vue'
import AppBreadcrumb from '@/components/common/AppBreadcrumb.vue'
import FullScreenLoader from '@/components/common/FullScreenLoader.vue'
import { 
  ArrowRight, Stethoscope, FileText, HeartPulse, ListCollapse, 
  RotateCcw, Printer, Thermometer, Wind, Ear, Siren, Droplets, Info,
  CheckSquare, Check, BrainCircuit, CheckCircle2, List, Microscope, AlertTriangle, Save
} from 'lucide-vue-next'

const router = useRouter()
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

const selectedGejalaDetails = computed(() => {
  return selectedGejala.value.map(id => {
    return gejalaList.value.find(g => g.id === id)
  }).filter(Boolean)
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

const saveRiwayatManual = () => {
  // Riwayat is automatically saved in backend during runDiagnosa
  router.push('/user/riwayat')
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
