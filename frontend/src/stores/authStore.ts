import { defineStore } from 'pinia'
import { apiFetch } from '@/utils/api'
import type { AuthState, UserCreate, Token } from '@/types/auth'

export const useAuthStore = defineStore('auth', {
  state: (): AuthState & { verifyPromise: Promise<void> | null } => ({
    user: null,
    token: localStorage.getItem('access_token'),
    isInitialized: false,
    isVerified: false,
    verifyPromise: null,
  }),

  getters: {
    isLoggedIn: (state): boolean => !!state.token,
    isAuthenticated: (state): boolean => !!state.token && state.isVerified,
  },

  actions: {
    /**
     * Client side Login logic: Updates state and persists the token.
     */
    login(access_token: string, username: string) {
      this.token = access_token
      this.user = username
      localStorage.setItem('access_token', access_token)

      // Reset verification flags so the next route guard triggers verifySession
      this.isInitialized = false
      this.isVerified = false
      this.verifyPromise = null
    },
    /**
     * Backend request to login a user.
     */
    async loginRequest(email: string, pass: string, remember: boolean): Promise<void> {
      const formData = new FormData()
      formData.append('username', email)
      formData.append('password', pass)

      const data = await apiFetch<Token>(`/auth/login?remember_me=${remember}`, {
        method: 'POST',
        body: formData,
      })

      this.login(data.access_token, data.display_name)
    },

    /**
     * Register a new user.
     * On success, it automatically logs the user in.
     */
    async registerRequest(userData: UserCreate, remember: boolean = false): Promise<boolean> {
      const data = await apiFetch<Token>(`/auth/register?remember_me=${remember}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
      })

      // Call the internal login action to keep state consistent
      this.login(data.access_token, data.display_name)

      return true
    },

    /**
     * Clears local state and storage.
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
        } catch (error) {
          this.logout()
          throw error
        } finally {
          this.verifyPromise = null
        }
      })()

      return this.verifyPromise
    },
  },
})
