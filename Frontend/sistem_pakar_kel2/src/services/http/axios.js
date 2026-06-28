import axios from 'axios'
import NProgress from 'nprogress'
import 'nprogress/nprogress.css'
import { appConfig } from '@/config/app'

// Configure NProgress
NProgress.configure({ showSpinner: false })

const httpClient = axios.create({
  baseURL: appConfig.apiUrl,
  headers: {
    'Content-Type': 'application/json',
    Accept: 'application/json'
  },
  timeout: 10000 // 10s timeout
})

// Track active requests to hide loading indicator when all are done
let activeRequests = 0

const startLoading = () => {
  if (activeRequests === 0) {
    NProgress.start()
    // We can also trigger global loading store here if registered
  }
  activeRequests++
}

const stopLoading = () => {
  activeRequests--
  if (activeRequests <= 0) {
    activeRequests = 0
    NProgress.done()
  }
}

// Request Interceptor
httpClient.interceptors.request.use(
  (config) => {
    startLoading()
    
    // Add auth token if available in local session
    const sessionStr = localStorage.getItem('sp_kel2_session')
    if (sessionStr) {
      try {
        const session = JSON.parse(sessionStr)
        if (session && session.token) {
          config.headers['Authorization'] = `Bearer ${session.token}`
        }
      } catch (e) {
        console.error('Error parsing session token:', e)
      }
    }
    return config
  },
  (error) => {
    stopLoading()
    return Promise.reject(error)
  }
)

// Response Interceptor
httpClient.interceptors.response.use(
  (response) => {
    stopLoading()
    return response.data
  },
  (error) => {
    stopLoading()
    
    const status = error.response ? error.response.status : null
    let errorMsg = 'Terjadi kesalahan pada sistem.'
    
    if (error.response && error.response.data) {
      errorMsg = error.response.data.detail || error.response.data.message || errorMsg
    } else if (error.message === 'Network Error') {
      errorMsg = 'Tidak dapat terhubung ke server. Periksa koneksi internet Anda.'
    }
    
    // Global Error Boundaries
    if (status === 401) {
      // Clear local session & redirect to login
      localStorage.removeItem('sp_kel2_session')
      window.location.href = '/login'
    } else if (status === 403) {
      errorMsg = 'Anda tidak memiliki hak akses untuk tindakan ini.'
    }
    
    // Standardize error message throwing
    const normalizedError = new Error(errorMsg)
    normalizedError.status = status
    normalizedError.response = error.response
    
    return Promise.reject(normalizedError)
  }
)

export default httpClient
