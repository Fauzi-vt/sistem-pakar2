<template>
  <div class="bg-[#f8f9ff] min-h-screen flex text-[#0d1c2e] antialiased">
    <!-- Split Screen Container -->
    <div class="flex w-full min-h-screen">
      
      <!-- Left Pane: Imagery & Brand Anchor (Hidden on smaller screens) -->
      <div class="hidden lg:flex lg:w-1/2 relative bg-[#1a365d] items-center justify-center overflow-hidden">
        <!-- Background Image -->
        <div class="absolute inset-0 w-full h-full bg-cover bg-center opacity-90" 
             style="background-image: url('https://lh3.googleusercontent.com/aida-public/AB6AXuAuhyHXJcdmXoTLJxtlZeTwqv-88oeacsqTK7H-YbmLF3ybVQ4znRxVBxVyqhB4Ev-IDjkTiyY7t47iLpL6gRKp-_lhPvDqIbAJocxTZYpCnNxjvggUE6JV4aPMb1v3b4akhm0t_TOvgSf_RZqeXrMtYaGy8z3S61SYshR7BWmStt6dU7otrMPPT6f_VD_w1ypcap8d9niK5ZuyCWW4gU3DN5cxuj9cWQ17ls3BQOCWlWcv4Ic_1C_JvfWLsg5MrbfYK-k5CcaP16bB')"></div>
        <!-- Gradient Overlay for contrast -->
        <div class="absolute inset-0 bg-[#002045]/40 bg-gradient-to-t from-[#002045]/80 to-transparent z-10"></div>
        <!-- Floating Brand Element -->
        <div class="relative z-20 flex flex-col items-center justify-center p-12 text-center text-white">
          <div class="w-16 h-16 bg-white rounded-xl flex items-center justify-center shadow-lg mb-6">
            <span class="material-symbols-outlined icon-fill text-[#002045] text-4xl">medical_services</span>
          </div>
          <h2 class="font-bold text-3xl mb-4 text-white">ENT Expert System</h2>
          <p class="text-lg text-[#adc7f7] max-w-md">
            Precision diagnostics and advanced clinical management platform designed for specialized medical environments.
          </p>
        </div>
      </div>

      <!-- Right Pane: Registration Form -->
      <div class="w-full lg:w-1/2 flex items-center justify-center p-8 sm:p-12 xl:p-24 bg-[#f8f9ff] relative">
        <!-- Close Button to Landing Page -->
        <router-link to="/" class="absolute top-8 right-8 flex items-center justify-center w-9 h-9 rounded-full bg-white hover:bg-surface-container border border-outline-variant/60 text-on-surface-variant hover:text-on-surface transition-all cursor-pointer shadow-sm active:scale-95" title="Kembali ke Beranda">
          <span class="material-symbols-outlined text-[20px]">close</span>
        </router-link>
        <div class="w-full max-w-md flex flex-col gap-8">
          
          <!-- Mobile Brand Header (Visible only on mobile/tablet) -->
          <div class="flex lg:hidden items-center gap-3 mb-4">
            <div class="w-10 h-10 bg-[#002045] text-white rounded flex items-center justify-center shadow-sm">
              <span class="material-symbols-outlined icon-fill text-xl">medical_services</span>
            </div>
            <span class="font-bold text-lg text-[#002045]">ENT Expert System</span>
          </div>

          <!-- Header -->
          <div class="space-y-2">
            <h1 class="font-bold text-3xl text-[#002045]">Patient Registration</h1>
            <p class="text-sm text-[#43474e]">
              Enter your details to create a secure medical portal account.
            </p>
          </div>

          <!-- Success Alert -->
          <Transition name="slide-down">
            <div v-if="isSuccess" class="flex items-center gap-3 p-4 rounded border"
                 style="background:#e0f2f1; border-color:#00685f33">
              <span class="material-symbols-outlined text-[#00685f] text-lg">check_circle</span>
              <div>
                <p class="text-xs font-bold text-[#005049]">Registrasi Berhasil!</p>
                <p class="text-[10px] text-[#006a61]">Mengalihkan ke halaman login...</p>
              </div>
            </div>
          </Transition>

          <!-- Error Alert -->
          <Transition name="slide-down">
            <div v-if="errorMessage" class="flex items-start gap-3 p-4 rounded border"
                 style="background:#ffdad6; border-color:#ba1a1a33">
              <span class="material-symbols-outlined text-[#ba1a1a] text-lg flex-shrink-0 mt-0.5">warning</span>
              <p class="text-xs text-[#93000a]">{{ errorMessage }}</p>
            </div>
          </Transition>

          <!-- Form -->
          <form v-if="!isSuccess" @submit.prevent="handleRegister" class="space-y-5">
            <!-- Full Name -->
            <div class="space-y-1">
              <label class="block text-xs font-semibold uppercase tracking-wider text-[#43474e]" for="fullName">
                Full Name
              </label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-[#74777f]">
                  <span class="material-symbols-outlined">person</span>
                </div>
                <input class="w-full pl-10 pr-4 py-3 bg-white border border-[#c4c6cf] rounded text-[#0d1c2e] focus:outline-none focus:border-[#13696a] focus:ring-1 focus:ring-[#13696a] transition-colors" 
                       id="fullName" 
                       name="fullName" 
                       placeholder="John Doe" 
                       required 
                       v-model="formData.name"
                       type="text"/>
              </div>
            </div>

            <!-- Email Address -->
            <div class="space-y-1">
              <label class="block text-xs font-semibold uppercase tracking-wider text-[#43474e]" for="email">
                Email Address
              </label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-[#74777f]">
                  <span class="material-symbols-outlined">mail</span>
                </div>
                <input class="w-full pl-10 pr-4 py-3 bg-white border border-[#c4c6cf] rounded text-[#0d1c2e] focus:outline-none focus:border-[#13696a] focus:ring-1 focus:ring-[#13696a] transition-colors" 
                       id="email" 
                       name="email" 
                       placeholder="name@example.com" 
                       required 
                       v-model="formData.email"
                       type="email"/>
              </div>
            </div>

            <!-- Password -->
            <div class="space-y-1">
              <label class="block text-xs font-semibold uppercase tracking-wider text-[#43474e]" for="password">
                Password
              </label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-[#74777f]">
                  <span class="material-symbols-outlined">lock</span>
                </div>
                <input class="w-full pl-10 pr-10 py-3 bg-white border border-[#c4c6cf] rounded text-[#0d1c2e] focus:outline-none focus:border-[#13696a] focus:ring-1 focus:ring-[#13696a] transition-colors" 
                       id="password" 
                       name="password" 
                       placeholder="••••••••" 
                       required 
                       v-model="formData.password"
                       :type="showPassword ? 'text' : 'password'"/>
                <button class="absolute inset-y-0 right-0 pr-3 flex items-center text-[#74777f] hover:text-[#43474e]" 
                        type="button"
                        @click="showPassword = !showPassword">
                  <span class="material-symbols-outlined">{{ showPassword ? 'visibility_off' : 'visibility' }}</span>
                </button>
              </div>
            </div>

            <!-- Confirm Password -->
            <div class="space-y-1">
              <label class="block text-xs font-semibold uppercase tracking-wider text-[#43474e]" for="confirmPassword">
                Confirm Password
              </label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-[#74777f]">
                  <span class="material-symbols-outlined">lock_reset</span>
                </div>
                <input class="w-full pl-10 pr-10 py-3 bg-white border border-[#c4c6cf] rounded text-[#0d1c2e] focus:outline-none focus:border-[#13696a] focus:ring-1 focus:ring-[#13696a] transition-colors" 
                       id="confirmPassword" 
                       name="confirmPassword" 
                       placeholder="••••••••" 
                       required 
                       v-model="formData.confirm"
                       type="password"/>
              </div>
            </div>

            <!-- Terms Checkbox -->
            <div class="flex items-start mt-2">
              <div class="flex items-center h-5">
                <input class="w-4 h-4 text-[#13696a] bg-white border-[#c4c6cf] rounded focus:ring-[#13696a] focus:ring-2 cursor-pointer" 
                       id="terms" 
                       name="terms" 
                       required 
                       v-model="agreeTerms"
                       type="checkbox"/>
              </div>
              <div class="ml-3 text-sm">
                <label class="block text-xs text-[#43474e] cursor-pointer" for="terms">
                  I agree to the <a class="font-semibold text-[#13696a] hover:underline" href="#">Terms and Conditions</a> and <a class="font-semibold text-[#13696a] hover:underline" href="#">Privacy Policy</a>.
                </label>
              </div>
            </div>

            <!-- Submit Action -->
            <div class="pt-4">
              <button class="w-full flex justify-center py-3 px-4 border border-transparent rounded bg-[#002045] text-white text-sm font-semibold hover:bg-[#455f88] shadow-sm transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[#002045]" 
                      type="submit"
                      :disabled="isLoading">
                <span v-if="isLoading" class="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin mr-2"></span>
                <span>Daftar</span>
              </button>
            </div>
          </form>

          <!-- Footer Link -->
          <div class="text-center pt-2 border-t border-[#c4c6cf]/30 mt-4">
            <p class="text-xs text-[#43474e]">
              Sudah punya akun? 
              <router-link class="font-semibold text-[#13696a] hover:text-[#1a6d6e] transition-colors hover:underline" to="/login">
                Login
              </router-link>
            </p>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { authStore } from '../../stores/auth.js'

const router = useRouter()
const errorMessage = ref('')
const isLoading    = ref(false)
const isSuccess    = ref(false)
const showPassword = ref(false)
const agreeTerms   = ref(false)

const formData = reactive({ name: '', email: '', password: '', confirm: '' })

const handleRegister = async () => {
  errorMessage.value = ''
  if (!agreeTerms.value) { errorMessage.value = 'Anda harus menyetujui Syarat dan Ketentuan.'; return }
  if (formData.password.length < 6) { errorMessage.value = 'Kata sandi harus minimal 6 karakter.'; return }
  if (formData.password !== formData.confirm) { errorMessage.value = 'Konfirmasi kata sandi tidak cocok.'; return }
  isLoading.value = true
  try {
    const result = await authStore.register(formData.name, formData.email, formData.password)
    isLoading.value = false
    if (result.success) { isSuccess.value = true; setTimeout(() => router.push('/login'), 1500) }
    else errorMessage.value = result.error
  } catch {
    isLoading.value = false
    errorMessage.value = 'Terjadi kesalahan saat mendaftar.'
  }
}
</script>

<style scoped>
.glass-panel {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(226, 232, 240, 0.5);
}

.icon-fill {
  font-variation-settings: 'FILL' 1, 'wght' 400, 'GRAD' 0, 'opsz' 24;
}

.slide-down-enter-active { transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1); }
.slide-down-leave-active { transition: all 0.2s ease-in; }
.slide-down-enter-from   { opacity: 0; transform: translateY(-8px); }
.slide-down-leave-to     { opacity: 0; transform: translateY(-4px); }
</style>
