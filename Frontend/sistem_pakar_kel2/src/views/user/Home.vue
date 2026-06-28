<template>
  <div class="min-h-screen bg-[#f8f9ff] text-[#0b1c30] font-sans pt-16">
    <!-- TopNavBar -->
    <nav class="bg-white/80 backdrop-blur-md fixed top-0 w-full z-50 border-b border-[#bcc9c6]/30 shadow-sm">
      <div class="flex justify-between items-center h-16 px-8 max-w-7xl mx-auto">
        <div class="text-xl font-bold text-[#00685f]">
          THT Expert System
        </div>
        <div class="hidden md:flex space-x-6 text-sm font-semibold">
          <router-link to="/home" 
                       class="text-[#00685f] border-b-2 border-[#00685f] pb-1">
            Beranda
          </router-link>
          <router-link to="/diagnosa" 
                       class="text-[#3d4947] hover:text-[#00685f] transition-colors pb-1">
            Konsultasi
          </router-link>
          <template v-if="!isAuthenticated">
            <router-link to="/login" 
                         class="text-[#3d4947] hover:text-[#00685f] transition-colors pb-1">
              Masuk Portal
            </router-link>
          </template>
          <template v-else>
            <button @click="handleLogout" 
                    class="text-[#ba1a1a] hover:text-red-700 transition-colors pb-1 cursor-pointer">
              Keluar
            </button>
          </template>
        </div>
      </div>
    </nav>

    <!-- Hero Section -->
    <main class="max-w-7xl mx-auto px-8 py-16 md:py-24">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-12 items-center">
        <!-- Hero Text -->
        <div class="space-y-6">
          <h1 class="text-4xl md:text-5xl font-bold text-[#0b1c30] leading-tight">
            Sistem Pakar Diagnosa Penyakit THT
          </h1>
          <p class="text-lg text-[#3d4947] leading-relaxed">
            Diagnosa cerdas menggunakan Teorema Bayes untuk keputusan klinis cepat, akurat, dan terpercaya.
          </p>
          <div class="pt-4">
            <button @click="goToDiagnosa" 
                    class="bg-[#00685f] text-white hover:bg-[#005049] px-6 py-3 rounded-lg font-semibold transition-all duration-200 flex items-center gap-2 shadow-sm active:scale-95">
              <span>Mulai Konsultasi</span>
              <span class="material-symbols-outlined">arrow_forward</span>
            </button>
          </div>
        </div>

        <!-- Hero Image -->
        <div class="relative rounded-2xl overflow-hidden shadow-lg border border-[#bcc9c6]/30 bg-[#e5eeff] aspect-video md:aspect-[4/3]">
          <img class="object-cover w-full h-full absolute inset-0 opacity-90" 
               alt="A modern, high-tech medical clinic interior focusing on advanced diagnostic equipment." 
               src="https://lh3.googleusercontent.com/aida-public/AB6AXuDKtJkcCTuVGvbkIuygvzjz-j-IMbNH0H7ypq0c9z13cxacZRQd0F2C--u_IeWW8kDGaBQjD5CBFeGuIQzwf__8ZiNIyrNBM7veeQK1pmHmCN1sBwLaks8zy057NjkyR9Ziw6jz3npv67CqNOKBwJIJM-5inU1LDn2SG79dhCu7WqBrrqyPY8VQ-acbsQdHhulv-eH_pk7SQvzcP_dOj8R3GZzIVDdEUzK7Hw4NywaEW_6B05ucjA2C8tSbshHBlGNA75cJ9yshDLZj"/>
          <div class="absolute inset-0 bg-gradient-to-tr from-[#f8f9ff]/40 to-transparent"></div>
        </div>
      </div>

      <!-- Features Bento Grid -->
      <div class="mt-20 grid grid-cols-1 md:grid-cols-3 gap-6">
        <div class="bg-white rounded-xl p-6 border border-[#bcc9c6]/30 hover:shadow-md transition-shadow">
          <div class="bg-[#e5eeff] w-12 h-12 rounded-lg flex items-center justify-center mb-4 text-[#00685f]">
            <span class="material-symbols-outlined icon-fill">speed</span>
          </div>
          <h3 class="font-bold text-lg text-[#0b1c30] mb-2">Analisis Cepat</h3>
          <p class="text-xs leading-relaxed text-[#3d4947]">Hasil diagnosa instan menggunakan perhitungan probabilitas posterior Teorema Bayes.</p>
        </div>
        
        <div class="bg-white rounded-xl p-6 border border-[#bcc9c6]/30 hover:shadow-md transition-shadow">
          <div class="bg-[#e5eeff] w-12 h-12 rounded-lg flex items-center justify-center mb-4 text-[#00685f]">
            <span class="material-symbols-outlined icon-fill">verified_user</span>
          </div>
          <h3 class="font-bold text-lg text-[#0b1c30] mb-2">Akurasi Tinggi</h3>
          <p class="text-xs leading-relaxed text-[#3d4947]">Basis pengetahuan diverifikasi oleh spesialis THT profesional.</p>
        </div>
        
        <div class="bg-white rounded-xl p-6 border border-[#bcc9c6]/30 hover:shadow-md transition-shadow">
          <div class="bg-[#e5eeff] w-12 h-12 rounded-lg flex items-center justify-center mb-4 text-[#00685f]">
            <span class="material-symbols-outlined icon-fill">dataset</span>
          </div>
          <h3 class="font-bold text-lg text-[#0b1c30] mb-2">Data Komprehensif</h3>
          <p class="text-xs leading-relaxed text-[#3d4947]">Mencakup berbagai gejala dan penyakit THT umum hingga spesifik.</p>
        </div>
      </div>

      <!-- Riwayat Konsultasi Section (Only visible when logged in) -->
      <section v-if="isAuthenticated" class="mt-20 space-y-6">
        <div class="flex items-center justify-between">
          <div>
            <div class="flex items-center gap-2">
              <div class="w-1.5 h-6 rounded-full bg-[#00685f]"></div>
              <h2 class="text-xl font-bold text-[#0b1c30]">Riwayat Konsultasi</h2>
            </div>
            <p class="text-xs text-[#6d7a77] pl-4 mt-1">Diagnosa terakhir Anda</p>
          </div>
          <button @click="goToDiagnosa"
                  class="flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-bold text-white transition-all shadow-md active:scale-95"
                  style="background:#00685f; box-shadow:0 4px 12px rgba(0,104,95,0.25)"
                  @mouseover="e => e.currentTarget.style.background='#005049'"
                  @mouseleave="e => e.currentTarget.style.background='#00685f'">
            <span class="material-symbols-outlined text-[18px]">add</span>
            <span>Konsultasi Baru</span>
          </button>
        </div>

        <!-- Empty state -->
        <div v-if="riwayatList.length === 0"
             class="bg-white rounded-2xl p-14 flex flex-col items-center gap-4 text-center border border-[#e5eeff]">
          <div class="w-16 h-16 rounded-2xl flex items-center justify-center border border-[#e5eeff]"
               style="background:#e0f2f1">
            <span class="material-symbols-outlined text-[#00685f] text-3xl">assignment_late</span>
          </div>
          <div>
            <p class="font-bold text-[#0b1c30]">Belum ada riwayat</p>
            <p class="text-xs text-[#6d7a77] mt-1">Mulai konsultasi pertama Anda sekarang!</p>
          </div>
        </div>

        <!-- Riwayat Cards List -->
        <div v-else class="space-y-3">
          <div v-for="(item, idx) in riwayatList" :key="item.id"
               class="group bg-white rounded-2xl p-5 border border-[#e5eeff] transition-all duration-300 cursor-pointer hover:shadow-lg hover:-translate-y-0.5"
               @mouseover="e => e.currentTarget.style.borderColor='rgba(0,104,95,0.3)'"
               @mouseleave="e => e.currentTarget.style.borderColor='#e5eeff'"
               @click="viewDetail(item)">
            <div class="flex items-start gap-4">
              <div class="w-10 h-10 rounded-xl flex items-center justify-center font-bold text-sm flex-shrink-0 bg-[#e5eeff] text-[#00685f]">
                {{ idx + 1 }}
              </div>

              <div class="flex-1 min-w-0">
                <div class="flex flex-wrap items-center gap-2 mb-2">
                  <p class="font-bold text-sm text-[#0b1c30]">{{ item.hasil }}</p>
                  <span class="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[10px] font-bold border"
                        :style="riwayatStatusStyle(item.status)">{{ item.status }}</span>
                </div>
                <p class="text-xs text-[#6d7a77] line-clamp-1 mb-2">{{ item.gejala }}</p>
                <div class="flex items-center gap-2">
                  <div class="flex-1 h-1.5 rounded-full overflow-hidden max-w-[160px] bg-[#e5eeff]">
                    <div class="h-full rounded-full transition-all duration-700 bg-gradient-to-r from-[#00685f] to-[#6bd8cb]"
                         :style="{width: `${Math.min(item.persentase,100)}%`}"></div>
                  </div>
                  <span class="text-xs font-bold tabular-nums text-[#00685f]">{{ item.persentase.toFixed(1) }}%</span>
                </div>
              </div>

              <div class="flex-shrink-0 text-right">
                <p class="text-xs text-[#6d7a77]">{{ item.tanggal }}</p>
                <span class="material-symbols-outlined text-[#bcc9c6] mt-2 block transition-colors group-hover:text-[#00685f]">
                  chevron_right
                </span>
              </div>
            </div>
          </div>
        </div>
      </section>
    </main>

    <!-- Detail Riwayat Modal -->
    <Transition name="fade">
      <div v-if="detailModalOpen" class="fixed inset-0 z-50 flex items-center justify-center p-4">
        <div @click="detailModalOpen = false" class="absolute inset-0 bg-[#0d1c2e]/60 backdrop-blur-sm"></div>
        <div class="relative w-full max-w-lg bg-white rounded-xl shadow-2xl overflow-hidden border border-[#c4c6cf]/30">
          <div class="flex justify-between items-center px-6 py-4 border-b border-[#c4c6cf]/20 bg-[#f8f9ff]">
            <h3 class="font-bold text-[#0d1c2e] flex items-center gap-2">
              <span class="material-symbols-outlined text-[#00685f]">assignment</span>
              Detail Diagnosa THT
            </h3>
            <button @click="detailModalOpen = false" class="text-[#74777f] hover:text-[#0d1c2e]">
              <span class="material-symbols-outlined text-lg">close</span>
            </button>
          </div>
          <div class="p-6 space-y-4 text-sm" v-if="selectedRiwayat">
            <div class="grid grid-cols-2 gap-4">
              <div>
                <p class="text-xs font-semibold text-[#74777f] uppercase">Tanggal Konsultasi</p>
                <p class="font-bold text-[#0d1c2e] mt-1">{{ selectedRiwayat.tanggal }}</p>
              </div>
              <div>
                <p class="text-xs font-semibold text-[#74777f] uppercase">Tingkat Kepercayaan</p>
                <p class="font-bold text-[#00685f] mt-1">{{ selectedRiwayat.persentase.toFixed(1) }}%</p>
              </div>
            </div>
            <div>
              <p class="text-xs font-semibold text-[#74777f] uppercase">Diagnosa Penyakit</p>
              <p class="font-bold text-lg text-[#0d1c2e] mt-1">{{ selectedRiwayat.hasil }}</p>
            </div>
            <div>
              <p class="text-xs font-semibold text-[#74777f] uppercase">Gejala yang Dipilih</p>
              <p class="font-medium text-[#43474e] mt-1 leading-relaxed">{{ selectedRiwayat.gejala }}</p>
            </div>
          </div>
        </div>
      </div>
    </Transition>

    <footer class="border-t border-[#bcc9c6]/30 py-6 bg-white text-center">
      <p class="text-xs text-[#74777f]">© 2026 Sistem Pakar THT — Kelompok 2 · RS Jasa Kartini. All rights reserved.</p>
    </footer>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth.store'
import { api } from '../../services/api.js'

const router = useRouter()
const authStore = useAuthStore()

const isAuthenticated = computed(() => authStore.isAuthenticated)
const userId          = computed(() => authStore.currentUser?.id || null)

const riwayatList      = ref([])
const detailModalOpen  = ref(false)
const selectedRiwayat  = ref(null)

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}

const goToDiagnosa = () => {
  router.push('/diagnosa')
}

const fetchRiwayat = async () => {
  if (!userId.value) return
  try {
    const res = await api.getRiwayatByUser(userId.value)
    if (res.success && Array.isArray(res.data)) {
      riwayatList.value = res.data.map(item => {
        // Parse hasil diagnosa JSON
        let diagnosaName = 'Tidak Ada'
        let percentage = 0.0
        let statusBayes = 'Tidak Ada'
        
        if (item.hasil_diagnosa && item.hasil_diagnosa.length > 0) {
          diagnosaName = item.hasil_diagnosa[0].nama_penyakit || 'Tidak Ada'
          percentage = item.hasil_diagnosa[0].persentase || 0.0
          statusBayes = item.hasil_diagnosa[0].status || 'Tidak Ada'
        }

        return {
          id: item.id,
          hasil: diagnosaName,
          persentase: percentage,
          status: statusBayes,
          gejala: item.gejala_names || 'Gejala tidak tercatat',
          tanggal: new Date(item.tanggal).toLocaleDateString('id-ID', { day: 'numeric', month: 'short', year: 'numeric' })
        }
      })
    }
  } catch (err) {
    console.error('Failed to fetch riwayat:', err)
  }
}

const riwayatStatusStyle = (status) => {
  if (status === 'Pasti') return 'background:#ffdad6; color:#93000a; border-color:#ba1a1a33'
  if (status === 'Hampir Pasti') return 'background:#fff3e0; color:#bf360c; border-color:rgba(230,81,0,0.2)'
  if (['Kemungkinan Besar','Sedang','Mungkin'].includes(status)) return 'background:#e0f2f1; color:#005049; border-color:rgba(0,104,95,0.25)'
  return 'background:#f8f9ff; color:#6d7a77; border-color:#e5eeff'
}

const viewDetail = (item) => {
  selectedRiwayat.value = item
  detailModalOpen.value = true
}

onMounted(() => {
  fetchRiwayat()
})
</script>

<style scoped>
.icon-fill {
  font-variation-settings: 'FILL' 1, 'wght' 400, 'GRAD' 0, 'opsz' 24;
}
.slide-down-enter-active { transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1); }
.slide-down-leave-active { transition: all 0.2s ease-in; }
.slide-down-enter-from   { opacity: 0; transform: translateY(-8px); }
.slide-down-leave-to     { opacity: 0; transform: translateY(-4px); }

.fade-enter-active, .fade-leave-active { transition: opacity 0.2s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>
