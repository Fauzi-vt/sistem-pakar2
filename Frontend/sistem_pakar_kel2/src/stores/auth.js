import { reactive } from 'vue'
import { api } from '../services/api.js'

const SESSION_KEY = 'sp_kel2_session'

function getSession() {
  try {
    return JSON.parse(localStorage.getItem(SESSION_KEY))
  } catch {
    return null
  }
}

export const authStore = reactive({
  currentUser: getSession(),

  /** Apakah pengguna sudah login */
  get isAuthenticated() {
    return !!this.currentUser
  },

  /** Apakah pengguna memiliki role admin */
  get isAdmin() {
    return this.currentUser?.role === 'admin'
  },

  /** Apakah pengguna memiliki role user */
  get isUser() {
    return this.currentUser?.role === 'user'
  },

  /**
   * Login dengan email & password via FastAPI/Supabase
   * @returns {Promise<{ success: boolean, user?: object, error?: string }>}
   */
  async login(email, password) {
    try {
      const response = await api.login(email, password)
      if (response.success && response.user) {
        const session = {
          id: response.user.id,
          name: response.user.name,
          email: response.user.email,
          role: response.user.role,
          token: response.user.token,
          avatar: response.user.name.charAt(0).toUpperCase(),
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

  /**
   * Registrasi akun baru via FastAPI/Supabase
   * @returns {Promise<{ success: boolean, error?: string }>}
   */
  async register(name, email, password) {
    try {
      const response = await api.register(name, email, password)
      if (response.success) {
        return { success: true }
      }
      return { success: false, error: 'Gagal melakukan pendaftaran.' }
    } catch (error) {
      return { success: false, error: error.message || 'Gagal melakukan pendaftaran.' }
    }
  },

  /** Logout dan hapus sesi */
  logout() {
    this.currentUser = null
    localStorage.removeItem(SESSION_KEY)
  },
})
