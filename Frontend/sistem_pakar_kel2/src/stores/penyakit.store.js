import { defineStore } from 'pinia'
import { penyakitApi } from '@/services/api/penyakit'

export const usePenyakitStore = defineStore('penyakit', {
  state: () => ({
    penyakitList: [],
    loading: false
  }),
  actions: {
    async fetchPenyakit() {
      this.loading = true
      try {
        const response = await penyakitApi.getAll()
        this.penyakitList = response.data || []
      } catch (error) {
        console.error(error)
        throw error
      } finally {
        this.loading = false
      }
    }
  }
})
