import httpClient from '@/services/http/axios'

export const gejalaApi = {
  getAll() {
    return httpClient.get('/api/gejala')
  },
  create(data) {
    return httpClient.post('/api/gejala', data)
  },
  update(id, data) {
    return httpClient.put(`/api/gejala/${id}`, data)
  },
  delete(id) {
    return httpClient.delete(`/api/gejala/${id}`)
  }
}
