import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth.store.js'
import authGuard from '@/middlewares/auth.js'
import guestGuard from '@/middlewares/guest.js'
import NProgress from 'nprogress'
import 'nprogress/nprogress.css'

NProgress.configure({ showSpinner: false })

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
      const authStore = useAuthStore()
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

router.beforeEach((to, from, next) => {
  NProgress.start()
  
  const authStore = useAuthStore()
  const isAuthenticated = authStore.isAuthenticated
  const userRole = authStore.currentUser?.role

  // If a logged-in user lands on `/`, redirect them to their respective home/dashboard
  if (to.path === '/' && isAuthenticated) {
    NProgress.done()
    return next(userRole === 'admin' ? '/admin/dashboard' : '/home')
  }

  // Admin and Auth middleware pipeline
  if (to.meta.requiresAuth) {
    return authGuard(to, from, (result) => {
      NProgress.done()
      if (result) {
        next(result)
      } else {
        next()
      }
    })
  }

  if (to.meta.guest) {
    return guestGuard(to, from, (result) => {
      NProgress.done()
      if (result) {
        next(result)
      } else {
        next()
      }
    })
  }

  next()
})

router.afterEach(() => {
  NProgress.done()
})

export default router
