import LoginPage from '@/pages/auth/LoginPage.vue'
import RegisterPage from '@/pages/auth/RegisterPage.vue'
import ContentPage from '@/pages/content/ContentPage.vue'
import AccountTab from '@/pages/content/tabs/AccountTab.vue'
import PredictTab from '@/pages/content/tabs/PredictTab.vue'
import DashboardTab from '@/pages/content/tabs/DashboardTab.vue'
import DatasetTab from '@/pages/content/tabs/DatasetTab.vue'
import InsightTab from '@/pages/content/tabs/ModelTab.vue'
import TrainTab from '@/pages/content/tabs/TrainTab.vue'
import UploadTab from '@/pages/content/tabs/UploadTab.vue'
import HeroSection from '@/components/layout/HeroSection.vue'
import LandingContainer from '@/pages/landing/LandingPage.vue'
import { useAuthStore } from '@/stores/credentials'
import { apiFetch } from '@/utils/api'
import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    component: LandingContainer,
    children: [
      { path: '', component: HeroSection },
      { path: 'login', component: LoginPage },
      { path: 'register', component: RegisterPage },
    ],
  },
  {
    path: '/app',
    component: ContentPage,
    meta: { requiresAuth: true },
    children: [
      { path: 'dashboard', name: 'dashboard', component: DashboardTab },
      { path: 'dataset', name: 'dataset', component: DatasetTab },
      { path: 'upload', name: 'upload', component: UploadTab },
      { path: 'train', name: 'train', component: TrainTab },
      { path: 'insight', name: 'insight', component: InsightTab },
      { path: 'predict', name: 'predict', component: PredictTab },
      { path: 'account', name: 'account', component: AccountTab },
    ],
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: routes,
})

router.beforeEach(async (to, from, next) => {
  const token = localStorage.getItem('access_token')
  const authStore = useAuthStore()

  if (to.meta.requiresAuth && !token) {
    return next('/login')
  }

  if (to.path === '/app' && token) {
    return next('/app/dashboard')
  }

  if (token) {
    try {
      await apiFetch<{ display_name: string; active_model: string }>('/auth/verify', {
        method: 'GET',
      })
      // token is valid → continue
      if (!to.path.startsWith('/app')) {
        return next('/app/dashboard')
      }
    } catch {
      console.log('No user matching the token exists')
      authStore.logout()
      return next('/')
    }
  }

  next()
})
export default router
