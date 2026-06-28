<template>
  <div class="bg-[#f8f9ff] min-h-screen flex text-[#0d1c2e] antialiased">
    <!-- Split Screen Layout -->
    <div class="flex w-full min-h-screen">

      <!-- Left Side: Image / Illustration (Hidden on small screens) -->
      <div class="hidden lg:flex lg:w-1/2 relative bg-[#eff4ff] items-center justify-center overflow-hidden">
        <!-- Background Image -->
        <div class="absolute inset-0 z-0">
          <img class="w-full h-full object-cover opacity-90"
               alt="A pristine, modern clinical environment featuring high-end medical equipment. The lighting is bright, soft, and hygienic white, emphasizing cleanliness and precision. Subtle teal accents in the room decor tie into the medical theme. The mood is calm, professional, and reassuring, suitable for a trusted diagnostic expert system."
               src="https://lh3.googleusercontent.com/aida-public/AB6AXuDWeGskwIs--Zdts5MalVdFNuzJsZv0qogI8nWUbPtKiDTncddTsBBqnfcGhBaAiZQVp11O4867tBP8riYuwBoMzczop5d2dV89erdBiQjDd7SEwP8AOdXtOi0-iDHsz9lxqLlZS1WlhS073KYF_tG7E0zJvrz8_036DLowoaHKupu5mmHijwmQJaqJeOm65OWcmpb_1Rn5Q_4WhKmO_GMvhxiz69KZdsNRv34B-vDgiKOH3St4RGMGq-dk9SX-377HYLolTkCn40g1"/>
        </div>
        <!-- Overlay for contrast -->
        <div class="absolute inset-0 bg-[#002045]/20 z-10"></div>
        <!-- Brand Badge -->
        <div class="absolute top-8 left-8 z-20 flex items-center gap-2 bg-white/80 backdrop-blur-md px-4 py-2 rounded-lg border border-[#c4c6cf]/30">
          <Stethoscope class="text-[#13696a] w-6 h-6" />
          <span class="font-bold text-lg text-[#002045]">ENT Expert System</span>
        </div>
        <!-- Motivational Quote / Proposition -->
        <div class="relative z-20 max-w-md p-8 bg-white/95 backdrop-blur-md rounded-xl shadow-lg border border-[#c4c6cf]/50 self-end mb-8 mr-8">
          <h2 class="font-bold text-xl text-[#002045] mb-2">Presisi Diagnostik</h2>
          <p class="text-sm leading-relaxed text-[#43474e]">Sistem terintegrasi untuk analisis spesialis THT. Mengutamakan akurasi data dan efisiensi alur kerja klinis.</p>
        </div>
      </div>

      <!-- Right Side: Login Form -->
      <div class="w-full lg:w-1/2 flex items-center justify-center p-8 relative">
        <!-- Close Button to Landing Page -->
        <router-link to="/" class="absolute top-8 right-8 flex items-center justify-center w-9 h-9 rounded-full bg-white hover:bg-surface-container border border-outline-variant/60 text-on-surface-variant hover:text-on-surface transition-all cursor-pointer shadow-sm active:scale-95" title="Kembali ke Beranda">
          <X class="w-5 h-5" />
        </router-link>
        <!-- Mobile Brand Header (Visible only on small screens) -->
        <div class="absolute top-8 left-8 lg:hidden flex items-center gap-2">
          <Stethoscope class="text-[#13696a] w-6 h-6" />
          <span class="font-bold text-lg text-[#002045]">ENT Expert</span>
        </div>

        <!-- Form Container -->
        <div class="w-full max-w-[420px] glass-panel rounded-xl p-6 shadow-sm">
          <div class="mb-6">
            <h1 class="font-bold text-3xl text-[#002045] mb-2">Selamat Datang</h1>
            <p class="text-sm text-[#43474e]">Silakan masuk untuk mengakses portal klinis Anda.</p>
          </div>

          <!-- Error Alert -->
          <Transition name="slide-down">
            <div v-if="errorMessage" class="mb-4 flex items-start gap-3 p-4 rounded-lg border"
                 style="background:#ffdad6; border-color:#ba1a1a33">
              <span class="material-symbols-outlined text-[#ba1a1a] text-lg flex-shrink-0 mt-0.5">warning</span>
              <p class="text-xs text-[#93000a]">{{ errorMessage }}</p>
            </div>
          </Transition>

          <form @submit.prevent="handleLogin" class="space-y-4">
            <!-- Email / Username Field -->
            <div class="flex flex-col gap-2">
              <label class="text-xs font-semibold text-[#002045]" for="identifier">Email / Nama Pengguna</label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <User class="text-[#74777f] w-5 h-5" />
                </div>
                <input class="input-clinical w-full pl-10 pr-4 py-2 bg-white border border-[#c4c6cf] rounded-lg text-[#0d1c2e] text-sm focus:outline-none focus:ring-0"
                       id="identifier"
                       name="identifier"
                       placeholder="dr.nama@klinik.com"
                       v-model="email"
                       type="text"/>
              </div>
              <p v-if="errors.email" class="text-xs text-[#ba1a1a] mt-1">{{ errors.email }}</p>
            </div>

            <!-- Password Field -->
            <div class="flex flex-col gap-2">
              <div class="flex justify-between items-center">
                <label class="text-xs font-semibold text-[#002045]" for="password">Kata Sandi</label>
                <a class="text-xs font-medium text-[#13696a] hover:text-[#1a6d6e] transition-colors" href="#">Lupa sandi?</a>
              </div>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <Lock class="text-[#74777f] w-5 h-5" />
                </div>
                <input class="input-clinical w-full pl-10 pr-10 py-2 bg-white border border-[#c4c6cf] rounded-lg text-[#0d1c2e] text-sm focus:outline-none focus:ring-0"
                       id="password"
                       name="password"
                       placeholder="••••••••"
                       v-model="password"
                       :type="showPassword ? 'text' : 'password'"/>
                <button class="absolute inset-y-0 right-0 pr-3 flex items-center text-[#74777f] hover:text-[#43474e] transition-colors"
                        type="button"
                        @click="showPassword = !showPassword">
                  <EyeOff v-if="showPassword" class="w-5 h-5" />
                  <Eye v-else class="w-5 h-5" />
                </button>
              </div>
              <p v-if="errors.password" class="text-xs text-[#ba1a1a] mt-1">{{ errors.password }}</p>
            </div>

            <!-- Remember Me -->
            <div class="flex items-center">
              <input class="h-4 w-4 text-[#13696a] focus:ring-[#13696a] border-[#c4c6cf] rounded bg-white cursor-pointer"
                     id="remember-me"
                     name="remember-me"
                     type="checkbox"
                     v-model="rememberMe"/>
              <label class="ml-2 block text-xs text-[#43474e] cursor-pointer" for="remember-me">
                Ingat saya di perangkat ini
              </label>
            </div>

            <!-- Login Button -->
            <div class="pt-2">
              <button class="btn-medical w-full flex justify-center items-center py-3 px-4 border border-transparent rounded-lg shadow-sm text-sm font-semibold text-white bg-[#1a365d] hover:bg-[#002045] focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[#1a365d]"
                      type="submit"
                      :disabled="isLoading">
                <span v-if="isLoading" class="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin mr-2"></span>
                <span>Masuk</span>
                <LogIn class="ml-2 w-5 h-5" />
              </button>
            </div>
          </form>

          <!-- Divider -->
          <div class="mt-6 relative">
            <div class="absolute inset-0 flex items-center">
              <div class="w-full border-t border-[#c4c6cf]/50"></div>
            </div>
            <div class="relative flex justify-center text-xs">
              <span class="px-2 bg-white text-[#43474e] font-medium">Atau</span>
            </div>
          </div>

          <!-- Registration Link -->
          <div class="mt-6 text-center">
            <p class="text-xs text-[#43474e]">
              Pasien baru?
              <router-link class="font-semibold text-[#13696a] hover:text-[#1a6d6e] transition-colors ml-1" to="/register">Daftar di sini</router-link>
            </p>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth.store'
import { useForm } from 'vee-validate'
import { loginSchema } from '@/schemas/login.schema'
import { Stethoscope, X, User, Lock, Eye, EyeOff, LogIn } from 'lucide-vue-next'

const router = useRouter()
const authStore = useAuthStore()
const errorMessage = ref('')
const isLoading    = ref(false)
const showPassword = ref(false)
const rememberMe   = ref(false)

const { handleSubmit, errors, defineField } = useForm({
  validationSchema: loginSchema
})

const [email] = defineField('email')
const [password] = defineField('password')

const handleLogin = handleSubmit(async (values) => {
  errorMessage.value = ''
  isLoading.value    = true
  try {
    const result = await authStore.login(values.email, values.password)
    isLoading.value = false
    if (result.success) {
      router.push(result.user.role === 'admin' ? '/admin/dashboard' : '/')
    } else {
      errorMessage.value = result.error
    }
  } catch (err) {
    isLoading.value    = false
    errorMessage.value = err.message || 'Terjadi kesalahan sistem.'
  }
})
</script>

<style scoped>
.glass-panel {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(226, 232, 240, 0.5);
}

.input-clinical {
  transition: all 0.2s ease;
}

.input-clinical:focus {
  border-color: #13696a;
  box-shadow: 0 0 0 2px rgba(19, 105, 106, 0.1);
}

.btn-medical {
  transition: all 0.2s ease;
}

.btn-medical:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(26, 54, 93, 0.1);
}

.slide-down-enter-active { transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1); }
.slide-down-leave-active { transition: all 0.2s ease-in; }
.slide-down-enter-from   { opacity: 0; transform: translateY(-8px); }
.slide-down-leave-to     { opacity: 0; transform: translateY(-4px); }
</style>
