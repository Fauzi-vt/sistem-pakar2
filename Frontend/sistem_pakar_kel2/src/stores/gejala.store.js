import { defineStore } from 'pinia'
import { gejalaApi } from '@/services/api/gejala'

export const useGejalaStore = defineStore('gejala', {
  state: () => ({
    gejalaList: [],
    loading: false
  }),
  actions: {
    async fetchGejala() {
      this.loading = true
      try {
        const response = await gejalaApi.getAll()
        this.gejalaList = response.data || []
      } catch (error) {
        console.error(error)
        throw error
      } finally {
        this.loading = false
      }
    }
  }
})
