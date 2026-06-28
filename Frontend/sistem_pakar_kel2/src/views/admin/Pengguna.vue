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
            <Menu class="w-5 h-5 text-on-surface" />
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
            <Search class="absolute left-3 top-1/2 -translate-y-1/2 text-on-surface-variant w-5 h-5" />
            <input 
              v-model="searchQuery"
              class="w-full bg-surface-container-lowest border border-outline-variant rounded pl-10 pr-4 py-2 font-body-sm text-on-surface focus:border-secondary focus:ring-1 focus:ring-secondary outline-none transition-all" 
              placeholder="Cari nama pengguna..." 
              type="text"
            />
          </div>
        </div>

        <!-- Users Data Table Card -->
        <section class="bg-surface-container-lowest border border-outline-variant rounded flex flex-col shadow-sm p-4">
          <DataTable :value="filteredUsers" :paginator="true" :rows="10" :loading="loading"
                     class="p-datatable-sm w-full text-sm" responsiveLayout="scroll">
            <template #empty>
              <div class="text-center py-6 text-on-surface-variant italic">
                Tidak ada data pengguna ditemukan
              </div>
            </template>
            <Column header="No" style="width: 80px">
              <template #body="slotProps">
                <span class="font-semibold text-primary">{{ slotProps.index + 1 }}</span>
              </template>
            </Column>
            <Column field="name" header="Nama Pengguna" :sortable="true">
              <template #body="slotProps">
                <span class="font-semibold text-on-surface">{{ slotProps.data.name || 'Anonim' }}</span>
              </template>
            </Column>
            <Column field="email" header="Email" :sortable="true"></Column>
            <Column field="role" header="Peran (Role)" :sortable="true">
              <template #body="slotProps">
                <span class="px-2.5 py-1 rounded-full text-xs font-bold border inline-block" 
                      :class="slotProps.data.role === 'admin' 
                        ? 'bg-[#E6F4EA] text-[#1E8E3E] border-[#1E8E3E]/20' 
                        : 'bg-surface-container text-on-surface-variant border-outline-variant/60'">
                  {{ slotProps.data.role.toUpperCase() }}
                </span>
              </template>
            </Column>
            <Column header="Aksi" style="text-align: right; width: 220px">
              <template #body="slotProps">
                <div class="flex items-center justify-end gap-2">
                  <button @click="toggleUserRole(slotProps.data)"
                          class="text-secondary hover:bg-surface-container-low px-2.5 py-1 rounded transition-colors cursor-pointer text-xs font-bold border border-secondary/20"
                          title="Ubah Peran">
                    Ubah ke {{ slotProps.data.role === 'admin' ? 'USER' : 'ADMIN' }}
                  </button>
                  <button @click="confirmDelete(slotProps.data)"
                          class="text-error hover:bg-error-container p-1.5 rounded transition-colors cursor-pointer"
                          title="Hapus Pengguna">
                    <Trash2 class="w-5 h-5 text-error" />
                  </button>
                </div>
              </template>
            </Column>
          </DataTable>
        </section>

      </main>

      <!-- Footer -->
      <footer class="border-t border-outline-variant px-6 py-4 bg-surface-container-lowest shrink-0">
        <p class="text-on-surface-variant text-xs text-center">© 2026 Sistem Pakar THT — Kelompok 2 · RS Jasa Kartini. All rights reserved.</p>
      </footer>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { usePenggunaStore } from '@/stores/pengguna.store'
import { useToast } from 'primevue/usetoast'
import { useConfirm } from 'primevue/useconfirm'
import Sidebar from '@/components/Sidebar.vue'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import { Search, Menu, Trash2 } from 'lucide-vue-next'

const sidebarOpen = ref(false)
const searchQuery = ref('')
const toast = useToast()
const confirm = useConfirm()

const penggunaStore = usePenggunaStore()
const users = computed(() => penggunaStore.users)
const loading = computed(() => penggunaStore.loading)

const filteredUsers = computed(() => {
  const q = searchQuery.value.trim().toLowerCase()
  if (!q) return users.value
  return users.value.filter(u => 
    (u.name && u.name.toLowerCase().includes(q)) ||
    (u.email && u.email.toLowerCase().includes(q))
  )
})

const fetchUsers = async () => {
  try {
    await penggunaStore.fetchUsers()
  } catch (err) {
    toast.add({ severity: 'error', summary: 'Gagal', detail: 'Gagal memuat pengguna: ' + err.message, life: 3000 })
  }
}

const toggleUserRole = async (user) => {
  const newRole = user.role === 'admin' ? 'user' : 'admin'
  try {
    const res = await penggunaStore.toggleUserRole(user.id, newRole)
    if (res.success) {
      toast.add({ severity: 'success', summary: 'Sukses', detail: `Peran ${user.name} berhasil diubah menjadi ${newRole.toUpperCase()}.`, life: 3000 })
    }
  } catch (err) {
    toast.add({ severity: 'error', summary: 'Gagal', detail: err.message, life: 3000 })
  }
}

const confirmDelete = (user) => {
  confirm.require({
    message: `Apakah Anda yakin ingin menghapus akun pengguna '${user.name}'? Tindakan ini permanen.`,
    header: 'Konfirmasi Hapus',
    icon: 'pi pi-exclamation-triangle',
    rejectClass: 'p-button-secondary p-button-outlined p-button-sm cursor-pointer',
    acceptClass: 'p-button-danger p-button-sm cursor-pointer',
    rejectLabel: 'Batal',
    acceptLabel: 'Hapus',
    accept: async () => {
      try {
        const res = await penggunaStore.deleteUser(user.id)
        if (res.success) {
          toast.add({ severity: 'success', summary: 'Sukses', detail: `Pengguna '${user.name}' berhasil dihapus.`, life: 3000 })
        }
      } catch (err) {
        toast.add({ severity: 'error', summary: 'Gagal', detail: err.message, life: 3000 })
      }
    }
  })
}

onMounted(fetchUsers)
</script>

<style scoped>
/* Specific styling overrides for PrimeVue DataTable elements if needed */
:deep(.p-datatable-header) {
  background: transparent;
  border: none;
}
:deep(.p-paginator) {
  background: transparent;
  border-top: 1px solid rgba(196, 198, 207, 0.3);
  padding-top: 1rem;
}
</style>
