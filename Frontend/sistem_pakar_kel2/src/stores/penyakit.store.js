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
    },
    async createPenyakit(payload) {
      try {
        const response = await penyakitApi.create(payload)
        if (response.success) {
          this.penyakitList.push(response.data)
        }
        return response
      } catch (error) {
        console.error(error)
        throw error
      }
    },
    async updatePenyakit(id, payload) {
      try {
        const response = await penyakitApi.update(id, payload)
        if (response.success) {
          const index = this.penyakitList.findIndex(p => p.id === id)
          if (index !== -1) {
            this.penyakitList[index] = { ...this.penyakitList[index], ...payload }
          }
        }
        return response
      } catch (error) {
        console.error(error)
        throw error
      }
    },
    async deletePenyakit(id) {
      try {
        const response = await penyakitApi.delete(id)
        if (response.success) {
          this.penyakitList = this.penyakitList.filter(p => p.id !== id)
        }
        return response
      } catch (error) {
        console.error(error)
        throw error
      }
    }
  }
})
