import { defineStore } from 'pinia'
import { authApi } from '@/services/api/auth'

const SESSION_KEY = 'sp_kel2_session'

function getSession() {
  try {
    return JSON.parse(localStorage.getItem(SESSION_KEY))
  } catch {
    return null
  }
}

export const useAuthStore = defineStore('auth', {
  state: () => ({
    currentUser: getSession()
  }),
  getters: {
    isAuthenticated: (state) => !!state.currentUser,
    isAdmin: (state) => state.currentUser?.role === 'admin',
    isUser: (state) => state.currentUser?.role === 'user'
  },
  actions: {
    async login(email, password) {
      try {
        const response = await authApi.login(email, password)
        if (response.success && response.user) {
          const session = {
            id: response.user.id,
            name: response.user.name,
            email: response.user.email,
            role: response.user.role,
            token: response.user.token,
            avatar: response.user.name.charAt(0).toUpperCase()
          }
          this.currentUser = session
          localStorage.setItem(SESSION_KEY, JSON.stringify(session))
          return { success: true, user: session }
        }
        return { success: false, error: 'Format data respon tidak valid.' }
      } catch (error) {
        return { success: false, error: error.message || 'Gagal masuk.' }
      }
    },
    async register(name, email, password) {
      try {
        const response = await authApi.register(name, email, password)
        if (response.success) {
          return { success: true }
        }
        return { success: false, error: 'Gagal melakukan pendaftaran.' }
      } catch (error) {
        return { success: false, error: error.message || 'Gagal melakukan pendaftaran.' }
      }
    },
    logout() {
      this.currentUser = null
      localStorage.removeItem(SESSION_KEY)
    }
  }
})
