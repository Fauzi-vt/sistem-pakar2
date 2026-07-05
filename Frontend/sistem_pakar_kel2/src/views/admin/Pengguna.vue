<template>
  <div class="min-h-screen bg-background text-on-background font-body-md flex relative antialiased">
    <!-- Side Navigation -->
    <Sidebar v-model:isOpen="sidebarOpen" />

    <!-- Main Content Area -->
    <div class="flex-1 flex flex-col min-h-screen lg:ml-64 transition-all duration-300">

      <!-- Header -->
      <header class="bg-surface-container-lowest dark:bg-surface-container flex justify-between items-center w-full px-container-padding h-16 sticky top-0 z-40 border-b border-outline-variant">
        <div class="flex items-center gap-4">
          <button @click="sidebarOpen = !sidebarOpen"
                  class="lg:hidden flex items-center justify-center p-2 bg-surface-container rounded-lg text-on-surface hover:bg-surface-container-high transition-colors">
            <Menu class="w-5 h-5" />
          </button>
          <div>
            <h1 class="font-headline-sm text-headline-sm font-bold text-primary leading-tight">Manajemen Pengguna</h1>
            <p class="text-xs text-on-surface-variant hidden sm:block mt-0.5">Kelola hak akses dan peran pengguna sistem</p>
          </div>
        </div>
        <!-- Refresh Button -->
        <button @click="fetchUsers"
                :disabled="loading"
                class="flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs font-semibold text-secondary border border-secondary/30 hover:bg-secondary/10 transition-all disabled:opacity-50 cursor-pointer">
          <RefreshCw class="w-3.5 h-3.5" :class="{ 'animate-spin': loading }" />
          <span class="hidden sm:inline">Perbarui</span>
        </button>
      </header>

      <!-- Main Canvas -->
      <main class="p-container-padding flex-1 flex flex-col gap-stack-lg">

        <!-- Error Banner -->
        <div v-if="error"
             class="flex items-center gap-3 p-4 bg-error-container text-on-error-container rounded-lg border border-error/20 text-sm">
          <AlertCircle class="w-5 h-5 shrink-0" />
          <span>{{ error }}</span>
          <button @click="fetchUsers" class="ml-auto text-xs underline font-bold cursor-pointer">Coba lagi</button>
        </div>

        <!-- Summary Cards -->
        <div class="grid grid-cols-2 sm:grid-cols-3 gap-gutter">
          <div class="bg-surface-container-lowest border border-outline-variant rounded-xl p-4 flex items-center gap-3 hover:shadow-md transition-all">
            <div class="p-2.5 rounded-lg bg-primary/10 text-primary shrink-0">
              <Users class="w-5 h-5" />
            </div>
            <div>
              <p class="text-xs text-on-surface-variant font-semibold uppercase tracking-wide">Total Pengguna</p>
              <p class="text-2xl font-bold text-primary">{{ users.length }}</p>
            </div>
          </div>
          <div class="bg-surface-container-lowest border border-outline-variant rounded-xl p-4 flex items-center gap-3 hover:shadow-md transition-all">
            <div class="p-2.5 rounded-lg bg-[#1E8E3E]/10 text-[#1E8E3E] shrink-0">
              <ShieldCheck class="w-5 h-5" />
            </div>
            <div>
              <p class="text-xs text-on-surface-variant font-semibold uppercase tracking-wide">Admin</p>
              <p class="text-2xl font-bold text-[#1E8E3E]">{{ adminCount }}</p>
            </div>
          </div>
          <div class="bg-surface-container-lowest border border-outline-variant rounded-xl p-4 flex items-center gap-3 hover:shadow-md transition-all">
            <div class="p-2.5 rounded-lg bg-secondary/10 text-secondary shrink-0">
              <User class="w-5 h-5" />
            </div>
            <div>
              <p class="text-xs text-on-surface-variant font-semibold uppercase tracking-wide">User Biasa</p>
              <p class="text-2xl font-bold text-secondary">{{ userCount }}</p>
            </div>
          </div>
        </div>

        <!-- Search & Filter Bar -->
        <div class="bg-surface-container-lowest border border-outline-variant rounded-xl p-4 flex flex-col sm:flex-row items-center gap-3">
          <!-- Search -->
          <div class="relative w-full sm:w-1/2">
            <Search class="absolute left-3 top-1/2 -translate-y-1/2 text-on-surface-variant w-4 h-4" />
            <input
              v-model="searchQuery"
              class="w-full bg-surface-container border border-outline-variant rounded-lg pl-9 pr-4 py-2 text-sm text-on-surface focus:border-secondary focus:ring-1 focus:ring-secondary outline-none transition-all"
              placeholder="Cari nama atau email pengguna..."
              type="text"
            />
          </div>
          <!-- Role Filter -->
          <div class="flex gap-2 flex-wrap">
            <button
              v-for="f in roleFilters" :key="f.value"
              @click="roleFilter = f.value"
              :class="[
                'px-3 py-1.5 rounded-full text-xs font-bold border transition-all cursor-pointer',
                roleFilter === f.value
                  ? 'bg-primary text-on-primary border-primary'
                  : 'bg-surface-container text-on-surface-variant border-outline-variant hover:border-primary/40'
              ]">
              {{ f.label }}
            </button>
          </div>
          <!-- Result count -->
          <span class="text-xs text-on-surface-variant ml-auto shrink-0">
            {{ filteredUsers.length }} pengguna ditemukan
          </span>
        </div>

        <!-- Users Table -->
        <section class="bg-surface-container-lowest border border-outline-variant rounded-xl shadow-sm overflow-hidden">
          <!-- Loading Skeleton -->
          <div v-if="loading" class="p-6 space-y-3">
            <div v-for="i in 5" :key="i"
                 class="flex items-center gap-4 animate-pulse">
              <div class="w-10 h-10 rounded-full bg-surface-container-high shrink-0"></div>
              <div class="flex-1 space-y-2">
                <div class="h-3 w-40 bg-surface-container-high rounded"></div>
                <div class="h-3 w-56 bg-surface-container-high rounded"></div>
              </div>
              <div class="h-6 w-16 bg-surface-container-high rounded-full"></div>
              <div class="h-8 w-28 bg-surface-container-high rounded"></div>
            </div>
          </div>

          <!-- Empty State -->
          <div v-else-if="filteredUsers.length === 0" class="flex flex-col items-center justify-center py-16 gap-3 text-on-surface-variant">
            <Users class="w-12 h-12 opacity-25" />
            <p class="text-sm font-medium">Tidak ada pengguna ditemukan</p>
            <p class="text-xs">Coba ubah filter atau kata kunci pencarian</p>
          </div>

          <!-- Table -->
          <div v-else class="overflow-x-auto">
            <table class="w-full text-sm">
              <thead>
                <tr class="border-b border-outline-variant bg-surface-container-low">
                  <th class="px-5 py-3 text-left text-xs font-bold text-on-surface-variant uppercase tracking-wide w-10">No</th>
                  <th class="px-5 py-3 text-left text-xs font-bold text-on-surface-variant uppercase tracking-wide">Pengguna</th>
                  <th class="px-5 py-3 text-left text-xs font-bold text-on-surface-variant uppercase tracking-wide hidden md:table-cell">Email</th>
                  <th class="px-5 py-3 text-left text-xs font-bold text-on-surface-variant uppercase tracking-wide">Peran</th>
                  <th class="px-5 py-3 text-right text-xs font-bold text-on-surface-variant uppercase tracking-wide">Aksi</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-outline-variant/50">
                <tr v-for="(user, idx) in filteredUsers" :key="user.id"
                    class="hover:bg-surface-container-low transition-colors group">
                  <!-- No -->
                  <td class="px-5 py-3.5">
                    <span class="text-xs font-bold text-on-surface-variant">{{ idx + 1 }}</span>
                  </td>
                  <!-- Pengguna (Avatar + Nama) -->
                  <td class="px-5 py-3.5">
                    <div class="flex items-center gap-3">
                      <div class="w-9 h-9 rounded-full flex items-center justify-center font-bold text-sm shrink-0"
                           :class="getAvatarClass(user.role)">
                        {{ getInitials(user.name) }}
                      </div>
                      <div class="min-w-0">
                        <p class="font-semibold text-on-surface truncate">{{ user.name || 'Anonim' }}</p>
                        <p class="text-xs text-on-surface-variant md:hidden truncate">{{ user.email }}</p>
                      </div>
                    </div>
                  </td>
                  <!-- Email -->
                  <td class="px-5 py-3.5 hidden md:table-cell">
                    <span class="text-on-surface-variant">{{ user.email }}</span>
                  </td>
                  <!-- Role Badge -->
                  <td class="px-5 py-3.5">
                    <span class="px-2.5 py-1 rounded-full text-xs font-bold border inline-flex items-center gap-1"
                          :class="user.role === 'admin'
                            ? 'bg-[#E6F4EA] text-[#1E8E3E] border-[#1E8E3E]/20'
                            : 'bg-surface-container text-on-surface-variant border-outline-variant/60'">
                      <component :is="user.role === 'admin' ? ShieldCheck : User" class="w-3 h-3" />
                      {{ user.role === 'admin' ? 'Admin' : 'User' }}
                    </span>
                  </td>
                  <!-- Actions -->
                  <td class="px-5 py-3.5">
                    <div class="flex items-center justify-end gap-2">
                      <!-- Edit Nama -->
                      <button @click="openEditModal(user)"
                              class="p-1.5 rounded-lg text-secondary hover:bg-secondary/10 transition-colors cursor-pointer"
                              title="Edit Nama">
                        <Pencil class="w-4 h-4" />
                      </button>
                      <!-- Toggle Role -->
                      <button @click="toggleUserRole(user)"
                              :disabled="isSelf(user) || roleLoading === user.id"
                              class="flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-xs font-bold border transition-all cursor-pointer disabled:opacity-40 disabled:cursor-not-allowed"
                              :class="user.role === 'admin'
                                ? 'text-[#B06000] border-[#B06000]/30 hover:bg-[#B06000]/10'
                                : 'text-[#1E8E3E] border-[#1E8E3E]/30 hover:bg-[#1E8E3E]/10'"
                              :title="isSelf(user) ? 'Tidak bisa mengubah peran diri sendiri' : 'Ubah Peran'">
                        <RefreshCw v-if="roleLoading === user.id" class="w-3 h-3 animate-spin" />
                        <ArrowLeftRight v-else class="w-3 h-3" />
                        {{ user.role === 'admin' ? '→ User' : '→ Admin' }}
                      </button>
                      <!-- Delete -->
                      <button @click="confirmDelete(user)"
                              :disabled="isSelf(user)"
                              class="p-1.5 rounded-lg text-error hover:bg-error-container transition-colors cursor-pointer disabled:opacity-40 disabled:cursor-not-allowed"
                              :title="isSelf(user) ? 'Tidak bisa menghapus akun sendiri' : 'Hapus Pengguna'">
                        <Trash2 class="w-4 h-4" />
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

    <!-- ── EDIT NAMA MODAL ── -->
    <Transition name="modal-fade">
      <div v-if="editModal.open"
           class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-on-surface/40 backdrop-blur-sm"
           @click.self="editModal.open = false">
        <div class="w-full max-w-sm bg-surface-container-lowest rounded-2xl shadow-2xl border border-outline-variant overflow-hidden">
          <!-- Modal Header -->
          <div class="flex items-center justify-between px-6 py-4 border-b border-outline-variant bg-surface-container-low">
            <h3 class="font-bold text-primary flex items-center gap-2 text-sm">
              <Pencil class="w-4 h-4 text-secondary" />
              Edit Nama Pengguna
            </h3>
            <button @click="editModal.open = false" class="text-on-surface-variant hover:text-on-surface cursor-pointer transition-colors">
              <X class="w-5 h-5" />
            </button>
          </div>
          <!-- Modal Body -->
          <div class="p-6 space-y-4">
            <div>
              <p class="text-xs font-semibold text-on-surface-variant uppercase mb-1">Pengguna</p>
              <p class="font-bold text-primary">{{ editModal.user?.email }}</p>
            </div>
            <div>
              <label class="block text-xs font-semibold text-on-surface-variant uppercase mb-1.5" for="edit-name">Nama Baru</label>
              <input
                id="edit-name"
                v-model="editModal.name"
                type="text"
                placeholder="Masukkan nama lengkap..."
                class="w-full bg-surface-container border border-outline-variant rounded-lg px-4 py-2.5 text-sm text-on-surface focus:border-secondary focus:ring-1 focus:ring-secondary outline-none transition-all"
                @keydown.enter="submitEdit"
                @keydown.esc="editModal.open = false"
              />
            </div>
          </div>
          <!-- Modal Footer -->
          <div class="px-6 pb-6 flex gap-2 justify-end">
            <button @click="editModal.open = false"
                    class="px-4 py-2 text-sm rounded-lg border border-outline-variant text-on-surface-variant hover:bg-surface-container-low transition-all cursor-pointer">
              Batal
            </button>
            <button @click="submitEdit"
                    :disabled="!editModal.name.trim() || editModal.loading"
                    class="px-4 py-2 text-sm font-bold rounded-lg bg-primary text-on-primary hover:bg-primary/90 transition-all disabled:opacity-50 cursor-pointer flex items-center gap-2">
              <RefreshCw v-if="editModal.loading" class="w-3.5 h-3.5 animate-spin" />
              Simpan
            </button>
          </div>
        </div>
      </div>
    </Transition>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { usePenggunaStore } from '@/stores/pengguna.store'
import { useAuthStore } from '@/stores/auth.store'
import { useToast } from 'primevue/usetoast'
import { useConfirm } from 'primevue/useconfirm'
import Sidebar from '@/components/Sidebar.vue'
import {
  Menu, Search, Trash2, Users, User, ShieldCheck,
  Pencil, X, RefreshCw, AlertCircle, ArrowLeftRight
} from 'lucide-vue-next'

const sidebarOpen  = ref(false)
const searchQuery  = ref('')
const roleFilter   = ref('all')
const roleLoading  = ref(null)   // user.id saat sedang update role
const error        = ref(null)
const toast        = useToast()
const confirm      = useConfirm()

const authStore    = useAuthStore()
const penggunaStore = usePenggunaStore()

const users   = computed(() => penggunaStore.users)
const loading = computed(() => penggunaStore.loading)

// ── Filter helpers ─────────────────────────────────────
const roleFilters = [
  { value: 'all',   label: 'Semua' },
  { value: 'admin', label: 'Admin' },
  { value: 'user',  label: 'User' },
]

const filteredUsers = computed(() => {
  let list = users.value
  if (roleFilter.value !== 'all') {
    list = list.filter(u => u.role === roleFilter.value)
  }
  const q = searchQuery.value.trim().toLowerCase()
  if (q) {
    list = list.filter(u =>
      (u.name  && u.name.toLowerCase().includes(q)) ||
      (u.email && u.email.toLowerCase().includes(q))
    )
  }
  return list
})

const adminCount = computed(() => users.value.filter(u => u.role === 'admin').length)
const userCount  = computed(() => users.value.filter(u => u.role !== 'admin').length)

// ── Utility ────────────────────────────────────────────
const isSelf = (user) => authStore.currentUser?.id === user.id

const getInitials = (name) => {
  if (!name) return '?'
  const parts = name.trim().split(/\s+/)
  return parts.length >= 2
    ? (parts[0][0] + parts[1][0]).toUpperCase()
    : parts[0].substring(0, 2).toUpperCase()
}

const AVATAR_CLASSES = [
  'bg-primary text-on-primary',
  'bg-secondary text-on-secondary',
  'bg-tertiary text-on-tertiary',
  'bg-[#1E8E3E] text-white',
]
const getAvatarClass = (role) =>
  role === 'admin' ? 'bg-[#1E8E3E] text-white' : 'bg-secondary/20 text-secondary'

// ── Fetch ──────────────────────────────────────────────
const fetchUsers = async () => {
  error.value = null
  try {
    await penggunaStore.fetchUsers()
  } catch (err) {
    error.value = 'Gagal memuat data pengguna: ' + (err.message || 'Kesalahan server.')
    toast.add({ severity: 'error', summary: 'Gagal Memuat', detail: error.value, life: 4000 })
  }
}

// ── Toggle Role ────────────────────────────────────────
const toggleUserRole = async (user) => {
  if (isSelf(user)) return
  const newRole = user.role === 'admin' ? 'user' : 'admin'
  roleLoading.value = user.id
  try {
    const res = await penggunaStore.toggleUserRole(user.id, newRole)
    if (res.success) {
      toast.add({
        severity: 'success',
        summary: 'Berhasil',
        detail: `Peran ${user.name} diubah menjadi ${newRole.toUpperCase()}.`,
        life: 3000
      })
    }
  } catch (err) {
    toast.add({ severity: 'error', summary: 'Gagal', detail: err.message, life: 3000 })
  } finally {
    roleLoading.value = null
  }
}

// ── Delete ─────────────────────────────────────────────
const confirmDelete = (user) => {
  if (isSelf(user)) return
  confirm.require({
    message: `Hapus akun pengguna "${user.name || user.email}"? Tindakan ini permanen dan tidak dapat dibatalkan.`,
    header: 'Konfirmasi Hapus Pengguna',
    icon: 'pi pi-exclamation-triangle',
    rejectClass: 'p-button-secondary p-button-outlined p-button-sm cursor-pointer',
    acceptClass: 'p-button-danger p-button-sm cursor-pointer',
    rejectLabel: 'Batal',
    acceptLabel: 'Hapus Permanen',
    accept: async () => {
      try {
        const res = await penggunaStore.deleteUser(user.id)
        if (res.success) {
          toast.add({
            severity: 'success',
            summary: 'Berhasil Dihapus',
            detail: `Pengguna "${user.name}" berhasil dihapus dari sistem.`,
            life: 3000
          })
        }
      } catch (err) {
        toast.add({ severity: 'error', summary: 'Gagal Hapus', detail: err.message || 'Gagal menghapus pengguna.', life: 3000 })
      }
    }
  })
}

// ── Edit Nama Modal ────────────────────────────────────
const editModal = ref({
  open: false,
  user: null,
  name: '',
  loading: false,
})

const openEditModal = (user) => {
  editModal.value = { open: true, user, name: user.name || '', loading: false }
}

const submitEdit = async () => {
  if (!editModal.value.name.trim()) return
  editModal.value.loading = true
  try {
    const res = await penggunaStore.updateName(editModal.value.user.id, editModal.value.name.trim())
    if (res.success) {
      toast.add({
        severity: 'success',
        summary: 'Berhasil',
        detail: `Nama pengguna berhasil diperbarui.`,
        life: 3000
      })
      editModal.value.open = false
    }
  } catch (err) {
    toast.add({ severity: 'error', summary: 'Gagal', detail: err.message || 'Gagal memperbarui nama.', life: 3000 })
  } finally {
    editModal.value.loading = false
  }
}

onMounted(fetchUsers)
</script>

<style scoped>
.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.2s ease;
}
.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}
.modal-fade-enter-active .w-full,
.modal-fade-leave-active .w-full {
  transition: transform 0.2s ease;
}
.modal-fade-enter-from .w-full {
  transform: scale(0.95) translateY(-8px);
}
.modal-fade-leave-to .w-full {
  transform: scale(0.95) translateY(-8px);
}
</style>
