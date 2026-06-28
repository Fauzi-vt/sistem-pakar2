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
    }
  }
})
