import { defineStore } from 'pinia'
import { riwayatApi } from '@/services/api/riwayat'

export const useRiwayatStore = defineStore('riwayat', {
  state: () => ({
    riwayatList: [],
    recentList: [],   // 3 riwayat terakhir untuk dashboard
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
    async fetchByUser(userId) {
      this.loading = true
      try {
        const response = await riwayatApi.getByUser(userId)
        if (response.success && response.data) {
          this.riwayatList = response.data
          this.recentList  = response.data.slice(0, 3)
        }
        return response
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
          this.recentList  = this.recentList.filter(r => r.id !== id)
        }
        return response
      } catch (error) {
        console.error(error)
        throw error
      }
    }
  }
})
