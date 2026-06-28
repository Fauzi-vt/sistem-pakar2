import { defineStore } from 'pinia'
import { diagnosaApi } from '@/services/api/diagnosa'

export const useDiagnosaStore = defineStore('diagnosa', {
  state: () => ({
    result: null,
    loading: false
  }),
  actions: {
    async runDiagnosa(userId, gejalaIds) {
      this.loading = true
      try {
        const response = await diagnosaApi.runDiagnosa(userId, gejalaIds)
        this.result = response
        return response
      } catch (error) {
        console.error(error)
        throw error
      } finally {
        this.loading = false
      }
    }
  }
})
