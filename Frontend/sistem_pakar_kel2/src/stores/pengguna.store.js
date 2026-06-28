import { defineStore } from 'pinia'
import { penggunaApi } from '@/services/api/pengguna'

export const usePenggunaStore = defineStore('pengguna', {
  state: () => ({
    users: [],
    loading: false
  }),
  actions: {
    async fetchUsers() {
      this.loading = true
      try {
        const response = await penggunaApi.getAll()
        this.users = response.data || []
      } catch (error) {
        console.error(error)
        throw error
      } finally {
        this.loading = false
      }
    },
    async toggleUserRole(id, newRole) {
      try {
        const response = await penggunaApi.updateRole(id, newRole)
        if (response.success) {
          const user = this.users.find(u => u.id === id)
          if (user) {
            user.role = newRole
          }
        }
        return response
      } catch (error) {
        console.error(error)
        throw error
      }
    },
    async deleteUser(id) {
      try {
        const response = await penggunaApi.delete(id)
        if (response.success) {
          this.users = this.users.filter(u => u.id !== id)
        }
        return response
      } catch (error) {
        console.error(error)
        throw error
      }
    }
  }
})
