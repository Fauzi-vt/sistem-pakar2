import { createRouter, createWebHistory } from 'vue-router'
import { authStore } from '../stores/auth.js'

const routes = [
  // ─── Guest Only ───────────────────────────────────────────────
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/auth/Login.vue'),
    meta: { guest: true }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/auth/Register.vue'),
    meta: { guest: true }
  },

  // ─── User Routes ──────────────────────────────────────────────
  {
    path: '/',
    name: 'Landing',
    component: () => import('../views/LandingPage.vue')
  },
  {
    path: '/home',
    name: 'UserHome',
    component: () => import('../views/user/Home.vue'),
    meta: { requiresAuth: true, role: 'user' }
  },
  {
    path: '/diagnosa',
    name: 'UserDiagnosa',
    component: () => import('../views/user/Diagnosa.vue'),
    meta: { requiresAuth: true, role: 'user' }
  },

  // ─── Admin Routes ─────────────────────────────────────────────
  {
    path: '/admin/dashboard',
    name: 'AdminDashboard',
    component: () => import('../views/admin/Dashboard.vue'),
    meta: { requiresAuth: true, role: 'admin' }
  },
  {
    path: '/admin/penyakit',
    name: 'AdminPenyakit',
    component: () => import('../views/admin/Penyakit.vue'),
    meta: { requiresAuth: true, role: 'admin' }
  },
  {
    path: '/admin/gejala',
    name: 'AdminGejala',
    component: () => import('../views/admin/Gejala.vue'),
    meta: { requiresAuth: true, role: 'admin' }
  },
  {
    path: '/admin/aturan',
    name: 'AdminAturan',
    component: () => import('../views/admin/Aturan.vue'),
    meta: { requiresAuth: true, role: 'admin' }
  },
  {
    path: '/admin/riwayat',
    name: 'AdminRiwayat',
    component: () => import('../views/admin/Riwayat.vue'),
    meta: { requiresAuth: true, role: 'admin' }
  },
  {
    path: '/admin/pengguna',
    name: 'AdminPengguna',
    component: () => import('../views/admin/Pengguna.vue'),
    meta: { requiresAuth: true, role: 'admin' }
  },
  {
    path: '/admin/kesehatan',
    name: 'AdminKesehatan',
    component: () => import('../views/admin/Kesehatan.vue'),
    meta: { requiresAuth: true, role: 'admin' }
  },
  {
    path: '/admin/statistik',
    name: 'AdminStatistik',
    component: () => import('../views/admin/Statistik.vue'),
    meta: { requiresAuth: true, role: 'admin' }
  },
  {
    path: '/admin/pengaturan',
    name: 'AdminPengaturan',
    component: () => import('../views/admin/Pengaturan.vue'),
    meta: { requiresAuth: true, role: 'admin' }
  },

  // ─── Fallback ─────────────────────────────────────────────────
  {
    path: '/:pathMatch(.*)*',
    redirect: () => {
      if (authStore.isAuthenticated) {
        return authStore.isAdmin ? '/admin/dashboard' : '/home'
      }
      return '/login'
    }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior: () => ({ top: 0 })
})

router.beforeEach((to) => {
  const isAuthenticated = authStore.isAuthenticated
  const userRole = authStore.currentUser?.role

  // If a logged-in user lands on `/`, redirect them to their respective home/dashboard
  if (to.path === '/' && isAuthenticated) {
    return userRole === 'admin' ? '/admin/dashboard' : '/home'
  }

  // Redirect unauthenticated users to login
  if (to.meta.requiresAuth && !isAuthenticated) {
    return '/login'
  }

  // Redirect authenticated users away from guest pages
  if (to.meta.guest && isAuthenticated) {
    return userRole === 'admin' ? '/admin/dashboard' : '/home'
  }

  // Redirect users who are accessing the wrong role's route
  if (to.meta.role && to.meta.role !== userRole) {
    return userRole === 'admin' ? '/admin/dashboard' : '/home'
  }
})

export default router
