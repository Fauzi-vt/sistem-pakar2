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
    },
    async createGejala(payload) {
      try {
        const response = await gejalaApi.create(payload)
        if (response.success) {
          this.gejalaList.push(response.data)
        }
        return response
      } catch (error) {
        console.error(error)
        throw error
      }
    },
    async updateGejala(id, payload) {
      try {
        const response = await gejalaApi.update(id, payload)
        if (response.success) {
          const index = this.gejalaList.findIndex(g => g.id === id)
          if (index !== -1) {
            this.gejalaList[index] = { ...this.gejalaList[index], ...payload }
          }
        }
        return response
      } catch (error) {
        console.error(error)
        throw error
      }
    },
    async deleteGejala(id) {
      try {
        const response = await gejalaApi.delete(id)
        if (response.success) {
          this.gejalaList = this.gejalaList.filter(g => g.id !== id)
        }
        return response
      } catch (error) {
        console.error(error)
        throw error
      }
    }
  }
})
