<template>
  <div class="min-h-screen bg-background text-on-background font-body-md flex relative antialiased">
    <!-- Side Navigation -->
    <Sidebar v-model:isOpen="sidebarOpen" />

    <!-- Main Content Area -->
    <div class="flex-1 flex flex-col min-h-screen lg:ml-64 transition-all duration-300">
      
      <!-- Top Navigation Header -->
      <header class="bg-surface-container-lowest dark:bg-surface-container flex justify-between items-center w-full px-container-padding h-16 sticky top-0 z-40 border-b border-outline-variant">
        <!-- Left Title info -->
        <div class="flex items-center gap-4 w-full lg:w-1/2">
          <button @click="sidebarOpen = !sidebarOpen" 
                  class="lg:hidden flex items-center justify-center p-2 bg-surface-container rounded-lg text-on-surface hover:bg-surface-container-high transition-colors">
            <span class="material-symbols-outlined">menu</span>
          </button>
          <div>
            <h1 class="font-headline-sm text-headline-sm font-bold text-primary truncate leading-tight">Manajemen Pengguna</h1>
            <p class="text-xs text-on-surface-variant hidden sm:block mt-0.5">Kelola hak akses dan peran pengguna sistem</p>
          </div>
        </div>
      </header>

      <!-- Main Canvas -->
      <main class="p-container-padding flex-1 flex flex-col gap-stack-lg">
        
        <!-- Search bar -->
        <div class="bg-surface-container-lowest border border-outline-variant rounded p-stack-md shadow-sm flex items-center justify-between">
          <div class="relative w-full sm:w-1/3 min-w-[250px]">
            <span class="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-on-surface-variant">search</span>
            <input 
              v-model="searchQuery"
              class="w-full bg-surface-container-lowest border border-outline-variant rounded pl-10 pr-4 py-2 font-body-sm text-on-surface focus:border-secondary focus:ring-1 focus:ring-secondary outline-none transition-all" 
              placeholder="Cari nama pengguna..." 
              type="text"
            />
          </div>
        </div>

        <!-- Users Data Table Card -->
        <section class="bg-surface-container-lowest border border-outline-variant rounded flex flex-col shadow-sm">
          <div class="overflow-x-auto w-full">
            <table class="w-full text-left border-collapse">
              <thead>
                <tr class="border-b-2 border-primary bg-background">
                  <th class="p-4 pl-6 font-label-sm text-label-sm text-on-surface-variant uppercase tracking-wider w-24">No</th>
                  <th class="p-4 font-label-sm text-label-sm text-on-surface-variant uppercase tracking-wider">Nama Pengguna</th>
                  <th class="p-4 font-label-sm text-label-sm text-on-surface-variant uppercase tracking-wider">Email</th>
                  <th class="p-4 font-label-sm text-label-sm text-on-surface-variant uppercase tracking-wider">Peran (Role)</th>
                  <th class="p-4 pr-6 font-label-sm text-label-sm text-on-surface-variant uppercase tracking-wider text-right w-44">Aksi Peran / Hapus</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-outline-variant/30">
                <tr v-if="loading">
                  <td colspan="5" class="p-12 text-center text-on-surface-variant">
                    <div class="flex items-center justify-center gap-2">
                      <span class="w-4 h-4 border-2 border-t-transparent rounded-full animate-spin border-primary"></span>
                      <span>Memuat data pengguna...</span>
                    </div>
                  </td>
                </tr>
                <tr v-else-if="filteredUsers.length === 0">
                  <td colspan="5" class="p-12 text-center text-on-surface-variant italic">Tidak ada data pengguna</td>
                </tr>
                
                <tr v-else v-for="(u, idx) in filteredUsers" :key="u.id"
                    class="border-b border-outline-variant bg-surface-container-lowest hover:bg-surface-container-low transition-colors group">
                  <!-- Index -->
                  <td class="p-4 pl-6 font-semibold text-primary">
                    {{ idx + 1 }}
                  </td>
                  
                  <!-- Nama -->
                  <td class="p-4 font-body-sm text-on-surface font-semibold">
                    {{ u.name || 'Anonim' }}
                  </td>
                  
                  <!-- Email -->
                  <td class="p-4 font-body-sm text-on-surface-variant">
                    {{ u.email || '-' }}
                  </td>
                  
                  <!-- Role -->
                  <td class="p-4">
                    <span class="px-2.5 py-1 rounded-full text-xs font-bold border" 
                          :class="u.role === 'admin' 
                            ? 'bg-[#E6F4EA] text-[#1E8E3E] border-[#1E8E3E]/20' 
                            : 'bg-surface-container text-on-surface-variant border-outline-variant/60'">
                      {{ u.role.toUpperCase() }}
                    </span>
                  </td>
                  
                  <!-- Aksi -->
                  <td class="p-4 pr-6 text-right">
                    <div class="flex items-center justify-end gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                      <!-- Toggle Role button -->
                      <button @click="toggleUserRole(u)"
                              class="text-secondary hover:bg-surface-container p-1.5 rounded transition-colors cursor-pointer text-xs font-bold border border-secondary/20"
                              title="Ubah Peran">
                         Ubah ke {{ u.role === 'admin' ? 'USER' : 'ADMIN' }}
                      </button>
                      
                      <!-- Delete user -->
                      <button @click="confirmDelete(u)"
                              class="text-error hover:bg-error-container p-1.5 rounded transition-colors cursor-pointer"
                              title="Hapus Pengguna">
                        <span class="material-symbols-outlined text-[20px]">delete</span>
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>

      </main>

      <!-- Footer -->
      <footer class="border-t border-outline-variant px-6 py-4 bg-surface-container-lowest shrink-0">
        <p class="text-on-surface-variant text-xs text-center">© 2026 Sistem Pakar THT — Kelompok 2 · RS Jasa Kartini. All rights reserved.</p>
      </footer>
    </div>

    <!-- ── CONFIRM DELETE MODAL ── -->
    <Transition name="modal-fade">
      <div v-if="deleteModalOpen" class="fixed inset-0 z-50 flex items-center justify-center p-4">
        <!-- Overlay -->
        <div @click="closeDeleteModal" class="absolute inset-0 bg-inverse-surface/60 backdrop-blur-sm"></div>

        <!-- Dialog Box -->
        <div class="relative w-full max-w-md bg-surface-container-lowest rounded-xl shadow-2xl overflow-hidden border border-outline-variant animate-modal-pop">
          <div class="p-6 text-center">
            <div class="w-14 h-14 rounded-full bg-error-container text-on-error-container flex items-center justify-center mx-auto mb-4 border border-error/20">
              <span class="material-symbols-outlined text-2xl text-error">delete</span>
            </div>

            <h3 class="font-bold text-lg mb-2 text-primary">Hapus Pengguna?</h3>
            <p class="text-sm mb-6 leading-relaxed text-on-surface-variant">
              Apakah Anda yakin ingin menghapus akun pengguna <strong class="text-primary">{{ userToDelete?.name }}</strong>?
              <br><span class="text-xs mt-1 block text-error font-semibold">Tindakan ini permanen dan tidak dapat dibatalkan.</span>
            </p>

            <div class="flex items-center justify-center gap-3">
              <button @click="closeDeleteModal" class="px-4 py-2 border border-outline-variant rounded font-semibold hover:bg-surface-container-low transition-colors cursor-pointer text-on-surface">
                Batal
              </button>
              <button @click="handleDelete" :disabled="submitting" class="px-5 py-2 bg-error text-on-tertiary font-bold rounded hover:bg-red-700 transition-all cursor-pointer active:scale-95 flex items-center gap-2">
                <span v-if="submitting" class="w-3.5 h-3.5 border-2 border-white border-t-transparent rounded-full animate-spin"></span>
                <span>Hapus</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </Transition>

    <!-- ── TOAST NOTIFICATIONS ── -->
    <div class="fixed bottom-6 right-6 z-50 flex flex-col gap-2.5 max-w-sm w-full">
      <TransitionGroup name="toast-list">
        <div v-for="toast in toasts" :key="toast.id" class="flex items-start gap-3 p-4 bg-surface-container-lowest rounded-xl border shadow-2xl transition-all duration-300 border-outline-variant/60">
          <div class="mt-0.5 shrink-0">
            <span v-if="toast.type === 'success'" class="material-symbols-outlined text-secondary">check_circle</span>
            <span v-else class="material-symbols-outlined text-error">error</span>
          </div>
          <div class="flex-1">
            <p class="text-sm font-bold leading-tight text-primary">{{ toast.type === 'success' ? 'Sukses' : 'Gagal' }}</p>
            <p class="text-xs mt-0.5 leading-relaxed text-on-surface-variant">{{ toast.message }}</p>
          </div>
          <button @click="removeToast(toast.id)" class="text-on-surface-variant hover:text-on-surface cursor-pointer shrink-0">
            <span class="material-symbols-outlined text-base">close</span>
          </button>
        </div>
      </TransitionGroup>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { api } from '../../services/api.js'
import Sidebar from '../../components/Sidebar.vue'

const sidebarOpen = ref(false)
const users = ref([])
const loading = ref(false)
const searchQuery = ref('')

const deleteModalOpen = ref(false)
const userToDelete = ref(null)
const submitting = ref(false)

const toasts = ref([])
let toastIdCounter = 0

// ── Computed Filtered Users ───────────────────────────────────
const filteredUsers = computed(() => {
  const q = searchQuery.value.trim().toLowerCase()
  if (!q) return users.value
  return users.value.filter(u => 
    (u.name && u.name.toLowerCase().includes(q)) ||
    (u.email && u.email.toLowerCase().includes(q))
  )
})

// ── Toast System ──────────────────────────────────────────────
const showToast = (type, message) => {
  const id = toastIdCounter++
  toasts.value.push({ id, type, message })
  setTimeout(() => removeToast(id), 4500)
}
const removeToast = (id) => { toasts.value = toasts.value.filter(t => t.id !== id) }

// ── API Operations ─────────────────────────────────────────────
const fetchUsers = async () => {
  loading.value = true
  try {
    const res = await api.getUsers()
    users.value = res.success ? res.data : []
  } catch (err) {
    showToast('error', 'Gagal memuat pengguna: ' + err.message)
  } finally {
    loading.value = false
  }
}

const toggleUserRole = async (user) => {
  const newRole = user.role === 'admin' ? 'user' : 'admin'
  try {
    const res = await api.updateUserRole(user.id, newRole)
    if (res.success) {
      showToast('success', `Peran ${user.name} berhasil diubah menjadi ${newRole.toUpperCase()}.`)
      await fetchUsers()
    }
  } catch (err) {
    showToast('error', err.message)
  }
}

const confirmDelete = (user) => {
  userToDelete.value = user
  deleteModalOpen.value = true
}

const closeDeleteModal = () => {
  if (!submitting.value) {
    deleteModalOpen.value = false
    userToDelete.value = null
  }
}

const handleDelete = async () => {
  if (!userToDelete.value) return
  submitting.value = true
  try {
    const res = await api.deleteUser(userToDelete.value.id)
    if (res.success) {
      showToast('success', `Pengguna '${userToDelete.value.name}' berhasil dihapus.`)
      deleteModalOpen.value = false
      userToDelete.value = null
      await fetchUsers()
    }
  } catch (err) {
    showToast('error', err.message)
  } finally {
    submitting.value = false
  }
}

onMounted(fetchUsers)
</script>

<style scoped>
.modal-fade-enter-active, .modal-fade-leave-active { transition: opacity 0.25s ease; }
.modal-fade-enter-from, .modal-fade-leave-to       { opacity: 0; }
@keyframes modal-pop {
  from { transform: scale(0.95); opacity: 0; }
  to   { transform: scale(1);   opacity: 1; }
}
.animate-modal-pop { animation: modal-pop 0.2s cubic-bezier(0.16, 1, 0.3, 1) forwards; }
.toast-list-enter-active { transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275); }
.toast-list-leave-active { transition: all 0.2s ease-in; position: absolute; }
.toast-list-enter-from   { transform: translateY(20px) scale(0.9); opacity: 0; }
.toast-list-leave-to     { transform: translateX(100px); opacity: 0; }
</style>
