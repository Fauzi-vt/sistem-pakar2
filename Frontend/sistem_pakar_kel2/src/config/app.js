export const appConfig = {
  name: 'MedExpert',
  apiUrl: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  storageTokenKey: 'sb-access-token' // matches supabase token key if standard, or authStore local storage key
}
