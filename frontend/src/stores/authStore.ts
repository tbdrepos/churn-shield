import { defineStore } from 'pinia'
import { apiFetch } from '@/utils/api'
import type { AuthState, UserCreate, Token, UserRead } from '@/types/auth'

interface UserSettings {
  active_model_id: string | null
  churn_threshold: number
}

interface MeResponse {
  user_info: UserRead
  settings: UserSettings
}

export const useAuthStore = defineStore('auth', {
  state: (): AuthState & {
    verifyPromise: Promise<void> | null
    settings: UserSettings | null
  } => ({
    user: null as UserRead | null,
    settings: null,
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
     * Pure local login (no API call)
     */
    login(access_token: string) {
      this.token = access_token
      localStorage.setItem('access_token', access_token)

      // force re-hydration
      this.isInitialized = false
      this.isVerified = false
      this.verifyPromise = null
      this.user = null
      this.settings = null
    },

    /**
     * Backend login
     */
    async loginRequest(email: string, pass: string, remember: boolean): Promise<void> {
      const formData = new FormData()
      formData.append('username', email)
      formData.append('password', pass)

      const token = await apiFetch<Token>(`/auth/login?remember_me=${remember}`, {
        method: 'POST',
        body: formData,
      })

      this.login(token.access_token)

      // hydrate ONCE
      await this.verifySession()
    },

    /**
     * Register
     */
    async registerRequest(userData: UserCreate, remember: boolean = false): Promise<boolean> {
      const data = await apiFetch<Token>(`/auth/register?remember_me=${remember}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
      })

      this.login(data.access_token)

      await this.verifySession()

      return true
    },

    /**
     * Logout
     */
    logout() {
      this.token = null
      this.user = null
      this.settings = null
      this.isInitialized = false
      this.isVerified = false
      this.verifyPromise = null

      localStorage.removeItem('access_token')
    },

    /**
     * Single source of truth for session hydration
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
          const data = await apiFetch<MeResponse>('/account/me', {
            method: 'GET',
          })

          this.user = data.user_info
          this.settings = data.settings
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

    /**
     * Update settings
     */
    async updateSettings(partial: Partial<UserSettings>) {
      const data = await apiFetch<UserSettings>('/account/settings', {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(partial),
      })

      this.settings = data
    },
  },
})
