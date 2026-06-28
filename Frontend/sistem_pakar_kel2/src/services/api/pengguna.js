import httpClient from '@/services/http/axios'

export const penggunaApi = {
  getAll() {
    return httpClient.get('/api/users')
  },
  updateRole(id, role) {
    return httpClient.put(`/api/users/${id}/role`, { role })
  },
  delete(id) {
    return httpClient.delete(`/api/users/${id}`)
  },
  updateProfile(id, data) {
    return httpClient.put(`/api/users/${id}/profile`, data)
  }
}
