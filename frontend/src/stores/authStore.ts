import { defineStore } from 'pinia'
import { apiFetch } from '@/utils/api'
import type { AuthState } from '@/types/auth'

export const useAuthStore = defineStore('auth', {
  state: (): AuthState & { verifyPromise: Promise<void> | null } => ({
    user: null,
    token: localStorage.getItem('access_token'),
    isInitialized: false, // Tracks if we've verified the session once
    isVerified: false,
    verifyPromise: null,
  }),

  getters: {
    isLoggedIn: (state): boolean => !!state.token,
    // Return user info only if the session has been validated
    isAuthenticated: (state): boolean => !!state.token && state.isVerified,
  },

  actions: {
    /**
     * Standard Login
     */
    login(access_token: string, username: string) {
      this.token = access_token
      this.user = username
      localStorage.setItem('access_token', access_token)
      // trigger post login verification
      this.isInitialized = false
      this.isVerified = false
      this.verifyPromise = null
    },

    /**
     * Clears local state and storage
     */
    logout() {
      this.token = null
      this.user = null
      this.isInitialized = false
      this.isVerified = false
      this.verifyPromise = null
      localStorage.removeItem('access_token')
    },

    /**
     * Validates the existing token with the backend.
     * Prevents redundant calls by checking isInitialized.
     */
    async verifySession() {
      if (!this.token) {
        this.logout()
        return
      }

      if (this.isInitialized) return

      if (this.verifyPromise) return this.verifyPromise

      this.isInitialized = true

      this.verifyPromise = (async () => {
        try {
          const data = await apiFetch<{ display_name: string }>('/auth/verify', {
            method: 'GET',
          })

          this.user = data.display_name
          this.isVerified = true
          this.isInitialized = true
        } catch (error) {
          this.logout()
          throw error
        } finally {
          // Clear the promise once finished (success or failure)
          this.verifyPromise = null
        }
      })()

      return this.verifyPromise
    },
  },
})
