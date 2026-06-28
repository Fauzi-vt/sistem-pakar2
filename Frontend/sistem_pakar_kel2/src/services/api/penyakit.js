import httpClient from '@/services/http/axios'

export const penyakitApi = {
  getAll() {
    return httpClient.get('/api/penyakit')
  },
  create(data) {
    return httpClient.post('/api/penyakit', data)
  },
  update(id, data) {
    return httpClient.put(`/api/penyakit/${id}`, data)
  },
  delete(id) {
    return httpClient.delete(`/api/penyakit/${id}`)
  }
}
