/**
 * useTheme.js — Global light/dark mode composable
 *
 * Strategy:
 *  - Reads saved preference from localStorage on first use.
 *  - Falls back to the OS/system prefers-color-scheme if no saved pref.
 *  - Applies/removes the `dark` class on <html> (required by Tailwind darkMode: 'class').
 *  - Exposes `isDark` (reactive ref) and `toggleTheme()` to any component.
 *  - Uses a module-level singleton so all components share the same state.
 */
import { ref, watchEffect } from 'vue'

const STORAGE_KEY = 'sp-tht-theme'

// ── Determine initial theme ──────────────────────────────────────
function getInitialTheme() {
  const saved = localStorage.getItem(STORAGE_KEY)
  if (saved) return saved === 'dark'
  // Fall back to OS preference
  return window.matchMedia('(prefers-color-scheme: dark)').matches
}

// ── Singleton state (shared across all useTheme() calls) ─────────
const isDark = ref(getInitialTheme())

// Apply class to <html> whenever isDark changes
watchEffect(() => {
  if (isDark.value) {
    document.documentElement.classList.add('dark')
  } else {
    document.documentElement.classList.remove('dark')
  }
  localStorage.setItem(STORAGE_KEY, isDark.value ? 'dark' : 'light')
})

// ── Public composable ────────────────────────────────────────────
export function useTheme() {
  const toggleTheme = () => {
    isDark.value = !isDark.value
  }

  return { isDark, toggleTheme }
}
