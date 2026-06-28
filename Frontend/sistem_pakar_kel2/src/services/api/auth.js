import httpClient from '@/services/http/axios'

export const authApi = {
  login(email, password) {
    return httpClient.post('/api/auth/login', { email, password })
  },
  register(name, email, password) {
    return httpClient.post('/api/auth/register', { name, email, password })
  },
  changePassword(data) {
    return httpClient.post('/api/auth/change-password', data)
  }
}
