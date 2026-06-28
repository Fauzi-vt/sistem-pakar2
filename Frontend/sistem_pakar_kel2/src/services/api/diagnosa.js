import httpClient from '@/services/http/axios'

export const diagnosaApi = {
  runDiagnosa(user_id, gejala_ids) {
    return httpClient.post('/api/diagnosa/', { user_id, gejala_ids })
  },
  
  // ── Aturan (Basis Pengetahuan) ─────────────────────────
  getAturan(penyakit_id = null) {
    const url = penyakit_id ? `/api/aturan?penyakit_id=${penyakit_id}` : '/api/aturan'
    return httpClient.get(url)
  },
  createAturan(data) {
    return httpClient.post('/api/aturan', data)
  },
  updateAturan(id, data) {
    return httpClient.put(`/api/aturan/${id}`, data)
  },
  deleteAturan(id) {
    return httpClient.delete(`/api/aturan/${id}`)
  },
  bulkSaveAturan(penyakit_id, rules) {
    return httpClient.post('/api/aturan/bulk', { penyakit_id, rules })
  },

  // ── Dashboard Overview ─────────────────────────────────
  getDashboardStats() {
    return httpClient.get('/api/dashboard/stats')
  }
}
