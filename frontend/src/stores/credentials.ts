import { defineStore } from 'pinia'
import type { AuthState } from '@/types/auth'

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({
    user: null,
    token: localStorage.getItem('access_token'),
  }),
  getters: {
    isLoggedIn: (state): boolean => !!state.token,
  },
  actions: {
    login(access_token: string, username: string) {
      this.token = access_token
      this.user = username
      localStorage.setItem('access_token', access_token)
    },

    logout() {
      this.token = null
      this.user = null
      localStorage.removeItem('access_token')
    },
  },
})
