<template>
  <UserLayout>
    <AppBreadcrumb :items="[{ label: 'Dashboard', to: '/user/dashboard' }, { label: 'Profil Akun' }]" />
    <PageHeader 
      title="Profil & Pengaturan Akun" 
      description="Kelola informasi identitas Anda dan pengaturan keamanan akun." 
    />

    <FullScreenLoader :isVisible="isSaving" title="Menyimpan Perubahan" message="Mohon tunggu sebentar..." />

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      
      <!-- Left Column: Read-Only Info & Activity -->
      <div class="lg:col-span-1 flex flex-col gap-6">
        
        <!-- Profile Summary Card -->
        <div class="bg-surface-container-lowest border border-outline-variant rounded-2xl p-6 flex flex-col items-center text-center shadow-sm">
          <div class="w-24 h-24 rounded-full bg-primary-container text-on-primary-container text-3xl font-bold flex items-center justify-center mb-4">
            {{ userInitial }}
          </div>
          <h2 class="font-headline-sm font-bold text-primary">{{ authStore.currentUser?.name }}</h2>
          <p class="font-body-sm text-on-surface-variant">{{ authStore.currentUser?.email }}</p>
          <span class="mt-3 inline-flex px-3 py-1 bg-secondary-container text-on-secondary-container rounded-full text-xs font-bold uppercase tracking-wide">
            {{ authStore.currentUser?.role }}
          </span>
        </div>

        <!-- Activity History Card -->
        <div class="bg-surface-container-lowest border border-outline-variant rounded-2xl overflow-hidden shadow-sm">
          <div class="bg-surface-container-low px-5 py-3 border-b border-outline-variant">
            <h3 class="font-label-md font-bold text-primary flex items-center gap-2">
              <span class="material-symbols-outlined text-[18px]">monitoring</span>
              Aktivitas Akun
            </h3>
          </div>
          <div class="divide-y divide-outline-variant/40">
            <div class="px-5 py-3 flex justify-between items-center">
              <span class="font-body-sm text-on-surface-variant">Tanggal Bergabung</span>
              <span class="font-label-md font-bold text-primary">23 Juni 2026</span>
            </div>
            <div class="px-5 py-3 flex justify-between items-center">
              <span class="font-body-sm text-on-surface-variant">Login Terakhir</span>
              <span class="font-label-md font-bold text-primary">Hari ini</span>
            </div>
            <div class="px-5 py-3 flex justify-between items-center">
              <span class="font-body-sm text-on-surface-variant">Total Diagnosa</span>
              <span class="font-label-md font-bold text-primary">{{ totalDiagnosa }} kali</span>
            </div>
          </div>
        </div>

      </div>

      <!-- Right Column: Edit Forms -->
      <div class="lg:col-span-2 flex flex-col gap-6">
        
        <!-- Edit Profile Form -->
        <div class="bg-surface-container-lowest border border-outline-variant rounded-2xl overflow-hidden shadow-sm">
          <div class="bg-surface-container-low px-6 py-4 border-b border-outline-variant">
            <h3 class="font-headline-sm font-bold text-primary">Informasi Pribadi</h3>
          </div>
          <form @submit.prevent="handleUpdateProfile" class="p-6 flex flex-col gap-5">
            <div>
              <label class="block font-label-md text-on-surface mb-2">Nama Lengkap</label>
              <input type="text" v-model="profileForm.name" required
                     class="w-full bg-surface border border-outline-variant rounded-lg px-4 py-2.5 font-body-sm text-on-surface focus:border-primary focus:ring-1 focus:ring-primary outline-none transition-colors" />
            </div>
            <div>
              <label class="block font-label-md text-on-surface mb-2">Email (Tidak dapat diubah)</label>
              <input type="email" :value="authStore.currentUser?.email" disabled
                     class="w-full bg-surface-container-low border border-outline-variant rounded-lg px-4 py-2.5 font-body-sm text-on-surface-variant cursor-not-allowed opacity-70" />
            </div>
            <div class="flex justify-end pt-2">
              <button type="submit" :disabled="!isProfileChanged"
                      class="bg-primary text-on-primary hover:bg-primary/90 disabled:bg-surface-container-high disabled:text-on-surface-variant px-6 py-2.5 rounded-lg font-label-md transition-colors shadow-sm cursor-pointer">
                Simpan Perubahan
              </button>
            </div>
          </form>
        </div>

        <!-- Change Password Form -->
        <div class="bg-surface-container-lowest border border-outline-variant rounded-2xl overflow-hidden shadow-sm">
          <div class="bg-surface-container-low px-6 py-4 border-b border-outline-variant flex items-center gap-2">
            <span class="material-symbols-outlined text-error">lock_reset</span>
            <h3 class="font-headline-sm font-bold text-error">Ganti Password</h3>
          </div>
          <form @submit.prevent="handleChangePassword" class="p-6 flex flex-col gap-5">
            
            <div v-if="passwordError" class="p-3 bg-error-container text-error rounded-lg font-body-sm border border-error/20">
              {{ passwordError }}
            </div>
            <div v-if="passwordSuccess" class="p-3 bg-tertiary-container text-tertiary rounded-lg font-body-sm border border-tertiary/20">
              Password berhasil diubah.
            </div>

            <div>
              <label class="block font-label-md text-on-surface mb-2">Password Saat Ini</label>
              <input type="password" v-model="passwordForm.current" required
                     class="w-full bg-surface border border-outline-variant rounded-lg px-4 py-2.5 font-body-sm text-on-surface focus:border-primary focus:ring-1 focus:ring-primary outline-none transition-colors" />
            </div>
            <div>
              <label class="block font-label-md text-on-surface mb-2">Password Baru</label>
              <input type="password" v-model="passwordForm.new" required minlength="6"
                     class="w-full bg-surface border border-outline-variant rounded-lg px-4 py-2.5 font-body-sm text-on-surface focus:border-primary focus:ring-1 focus:ring-primary outline-none transition-colors" />
            </div>
            <div>
              <label class="block font-label-md text-on-surface mb-2">Konfirmasi Password Baru</label>
              <input type="password" v-model="passwordForm.confirm" required minlength="6"
                     class="w-full bg-surface border border-outline-variant rounded-lg px-4 py-2.5 font-body-sm text-on-surface focus:border-primary focus:ring-1 focus:ring-primary outline-none transition-colors" />
            </div>
            
            <div class="flex justify-end pt-2">
              <button type="submit" 
                      class="bg-error hover:bg-error/90 text-white px-6 py-2.5 rounded-lg font-label-md transition-colors shadow-sm cursor-pointer flex items-center gap-2">
                Update Password
              </button>
            </div>
          </form>
        </div>

      </div>
    </div>
  </UserLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import UserLayout from '@/layouts/UserLayout.vue'
import AppBreadcrumb from '@/components/common/AppBreadcrumb.vue'
import PageHeader from '@/components/common/PageHeader.vue'
import FullScreenLoader from '@/components/common/FullScreenLoader.vue'
import { useAuthStore } from '@/stores/auth.store'
import { authApi } from '@/services/api/auth.js'
import { riwayatApi } from '@/services/api/riwayat'
import { useToast } from 'primevue/usetoast'

const authStore = useAuthStore()
const toast = useToast()

const isSaving = ref(false)
const totalDiagnosa = ref(0)
const passwordError = ref('')
const passwordSuccess = ref(false)

const profileForm = ref({
  name: authStore.currentUser?.name || ''
})

const passwordForm = ref({
  current: '',
  new: '',
  confirm: ''
})

const userInitial = computed(() => {
  if (authStore.currentUser?.name) {
    return authStore.currentUser.name.charAt(0).toUpperCase()
  }
  return 'U'
})

const isProfileChanged = computed(() => {
  return profileForm.value.name.trim() !== authStore.currentUser?.name
})

const fetchActivity = async () => {
  try {
    if (authStore.currentUser?.id) {
      const res = await riwayatApi.getByUser(authStore.currentUser.id)
      if (res.success && res.data) {
        totalDiagnosa.value = res.data.length
      }
    }
  } catch {
    // silently fail
  }
}

const handleUpdateProfile = async () => {
  if (!isProfileChanged.value) return
  
  isSaving.value = true
  try {
    // Simulating API Call since Supabase auth update might require token adjustments in backend
    // const res = await penggunaApi.updateProfile(authStore.currentUser.id, { name: profileForm.value.name })
    
    // Simulate delay
    await new Promise(r => setTimeout(r, 800))
    
    // Update local store
    authStore.currentUser.name = profileForm.value.name
    localStorage.setItem('sp_kel2_session', JSON.stringify(authStore.currentUser))
    
    // Success handling (could add Toast here)
  } catch (error) {
    console.error('Failed to update profile', error)
  } finally {
    isSaving.value = false
  }
}

const handleChangePassword = async () => {
  passwordError.value = ''
  passwordSuccess.value = false
  
  if (passwordForm.value.new !== passwordForm.value.confirm) {
    passwordError.value = 'Password baru dan konfirmasi tidak cocok.'
    return
  }

  isSaving.value = true
  try {
    const res = await authApi.changePassword({
      user_id: authStore.currentUser.id,
      current_password: passwordForm.value.current,
      new_password: passwordForm.value.new
    })

    if (res.success) {
      passwordSuccess.value = true
      passwordForm.value = { current: '', new: '', confirm: '' }
    } else {
      passwordError.value = res.error || 'Gagal mengubah password.'
    }
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Gagal', detail: error.message || 'Gagal mengubah password.', life: 3000 })
  } finally {
    isSaving.value = false
  }
}

onMounted(() => {
  fetchActivity()
})
</script>
