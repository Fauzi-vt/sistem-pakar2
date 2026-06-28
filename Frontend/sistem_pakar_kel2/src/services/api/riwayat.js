import httpClient from '@/services/http/axios'

export const riwayatApi = {
  getAll() {
    return httpClient.get('/api/riwayat')
  },
  delete(id) {
    return httpClient.delete(`/api/riwayat/${id}`)
  }
}
