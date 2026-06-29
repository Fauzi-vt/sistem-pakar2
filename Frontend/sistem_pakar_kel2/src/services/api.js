import { appConfig } from '@/config/app'
const BASE_URL = appConfig.apiUrl
async function request(path, options = {}) {
  const url = `${BASE_URL}${path}`
  const headers = { 'Content-Type': 'application/json', ...options.headers }
  const config = { ...options, headers }
  if (options.body && typeof options.body === 'object') {
    config.body = JSON.stringify(options.body)
  }
  try {
    const response = await fetch(url, config)
    const data = await response.json()
    if (!response.ok) throw new Error(data.detail || 'Terjadi kesalahan sistem.')
    return data
  } catch (error) {
    throw new Error(error.message || 'Tidak dapat terhubung ke server backend.', { cause: error })
  }
}

export const api = {
  // ── Auth ──────────────────────────────────────────────
  login(email, password) {
    return request('/api/auth/login', { method: 'POST', body: { email, password } })
  },
  register(name, email, password) {
    return request('/api/auth/register', { method: 'POST', body: { name, email, password } })
  },

  // ── Penyakit ──────────────────────────────────────────
  getPenyakit() {
    return request('/api/penyakit')
  },
  createPenyakit(data) {
    return request('/api/penyakit', { method: 'POST', body: data })
  },
  updatePenyakit(id, data) {
    return request(`/api/penyakit/${id}`, { method: 'PUT', body: data })
  },
  deletePenyakit(id) {
    return request(`/api/penyakit/${id}`, { method: 'DELETE' })
  },

  // ── Gejala ────────────────────────────────────────────
  getGejala() {
    return request('/api/gejala')
  },
  createGejala(data) {
    return request('/api/gejala', { method: 'POST', body: data })
  },
  updateGejala(id, data) {
    return request(`/api/gejala/${id}`, { method: 'PUT', body: data })
  },
  deleteGejala(id) {
    return request(`/api/gejala/${id}`, { method: 'DELETE' })
  },

  // ── Aturan (Basis Pengetahuan) ─────────────────────────
  getAturan(penyakit_id = null) {
    const path = penyakit_id ? `/api/aturan?penyakit_id=${penyakit_id}` : '/api/aturan'
    return request(path)
  },
  getAturanByPenyakit(penyakit_id) {
    return request(`/api/aturan?penyakit_id=${penyakit_id}`)
  },
  createAturan(data) {
    return request('/api/aturan', { method: 'POST', body: data })
  },
  updateAturan(id, data) {
    return request(`/api/aturan/${id}`, { method: 'PUT', body: data })
  },
  deleteAturan(id) {
    return request(`/api/aturan/${id}`, { method: 'DELETE' })
  },
  bulkSaveAturan(penyakit_id, rules) {
    // rules: [{ gejala_id, conditional_probability }]
    return request('/api/aturan/bulk', { method: 'POST', body: { penyakit_id, rules } })
  },

  // ── Diagnosa ──────────────────────────────────────────
  runDiagnosa(user_id, gejala_ids) {
    return request('/api/diagnosa/', { method: 'POST', body: { user_id, gejala_ids } })
  },

  // ── Riwayat Diagnosa ─────────────────────────────────────
  getRiwayat() {
    return request('/api/riwayat')
  },
  deleteRiwayat(id) {
    return request(`/api/riwayat/${id}`, { method: 'DELETE' })
  },

  // ── Users ────────────────────────────────────────────────
  getUsers() {
    return request('/api/users')
  },
  updateUserRole(id, role) {
    return request(`/api/users/${id}/role`, { method: 'PUT', body: { role } })
  },
  deleteUser(id) {
    return request(`/api/users/${id}`, { method: 'DELETE' })
  },

  // ── Dashboard ──────────────────────────────────────────
  getDashboardStats() {
    return request('/api/dashboard/stats')
  }
}
