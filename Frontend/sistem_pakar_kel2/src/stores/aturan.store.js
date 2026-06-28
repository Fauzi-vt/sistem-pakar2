import { defineStore } from 'pinia'
import { diagnosaApi } from '@/services/api/diagnosa'

export const useAturanStore = defineStore('aturan', {
  state: () => ({
    rules: [],
    loading: false
  }),
  actions: {
    async fetchRules(penyakitId = null) {
      this.loading = true
      try {
        const response = await diagnosaApi.getAturan(penyakitId)
        if (response.success && Array.isArray(response.data)) {
          this.rules = response.data.map(r => ({
            id: r.id,
            penyakit_id: r.penyakit_id,
            penyakit_kode: r.penyakit?.kode_penyakit || '?',
            penyakit_nama: r.penyakit?.nama_penyakit || '?',
            gejala_id: r.gejala_id,
            gejala_kode: r.gejala?.kode_gejala || '?',
            gejala_nama: r.gejala?.nama_gejala || '?',
            probability: r.conditional_probability ?? 0.0
          }))
        } else {
          this.rules = []
        }
      } catch (error) {
        console.error(error)
        throw error
      } finally {
        this.loading = false
      }
    },
    async createRule(payload) {
      try {
        const response = await diagnosaApi.createAturan(payload)
        return response
      } catch (error) {
        console.error(error)
        throw error
      }
    },
    async updateRule(id, payload) {
      try {
        const response = await diagnosaApi.updateAturan(id, payload)
        return response
      } catch (error) {
        console.error(error)
        throw error
      }
    },
    async deleteRule(id) {
      try {
        const response = await diagnosaApi.deleteAturan(id)
        if (response.success) {
          this.rules = this.rules.filter(r => r.id !== id)
        }
        return response
      } catch (error) {
        console.error(error)
        throw error
      }
    }
  }
})
