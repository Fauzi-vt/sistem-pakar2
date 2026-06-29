import httpClient from '@/services/http/axios'

export const riwayatApi = {
  getAll() {
    return httpClient.get('/api/riwayat')
  },
  delete(id) {
    return httpClient.delete(`/api/riwayat/${id}`)
  },
  getByUser(userId) {
    return httpClient.get(`/api/riwayat/user/${userId}`)
  },
  // alias agar konsisten dengan pemanggilan di UserDashboard
  getRiwayatByUser(userId) {
    return httpClient.get(`/api/riwayat/user/${userId}`)
  }
}
