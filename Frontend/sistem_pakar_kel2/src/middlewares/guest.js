import { useAuthStore } from '@/stores/auth.store'

export default function guestGuard(to, from, next) {
  const authStore = useAuthStore()
  if (authStore.isAuthenticated) {
    return next(authStore.isAdmin ? '/admin/dashboard' : '/home')
  }
  return next()
}
