import { useAuthStore } from '@/stores/auth.store'

export default function authGuard(to, from, next) {
  const authStore = useAuthStore()
  if (!authStore.isAuthenticated) {
    return next('/login')
  }
  
  // Role check
  if (to.meta.role && to.meta.role !== authStore.currentUser?.role) {
    return next(authStore.isAdmin ? '/admin/dashboard' : '/home')
  }
  
  return next()
}
