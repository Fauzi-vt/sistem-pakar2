import { defineStore } from 'pinia'
import { riwayatApi } from '@/services/api/riwayat'

export const useRiwayatStore = defineStore('riwayat', {
  state: () => ({
    riwayatList: [],
    loading: false
  }),
  actions: {
    async fetchRiwayat() {
      this.loading = true
      try {
        const response = await riwayatApi.getAll()
        this.riwayatList = response.data || []
      } catch (error) {
        console.error(error)
        throw error
      } finally {
        this.loading = false
      }
    },
    async deleteRiwayat(id) {
      try {
        const response = await riwayatApi.delete(id)
        if (response.success) {
          this.riwayatList = this.riwayatList.filter(r => r.id !== id)
        }
        return response
      } catch (error) {
        console.error(error)
        throw error
      }
    }
  }
})
