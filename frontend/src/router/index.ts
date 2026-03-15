import LoginPage from '@/components/auth/LoginPage.vue'
import RegisterPage from '@/components/auth/RegisterPage.vue'
import ContentPage from '@/components/content/ContentPage.vue'
import AccountTab from '@/components/content/tabs/AccountTab.vue'
import CustomersTab from '@/components/content/tabs/CustomersTab.vue'
import DashboardTab from '@/components/content/tabs/DashboardTab.vue'
import ModelTab from '@/components/content/tabs/ModelTab.vue'
import UploadTab from '@/components/content/tabs/UploadTab.vue'
import FeaturesSection from '@/components/landing/FeaturesSection.vue'
import HeroSection from '@/components/landing/HeroSection.vue'
import LandingContainer from '@/components/landing/LandingContainer.vue'
import PlansSection from '@/components/landing/PlansSection.vue'
import { useAuthStore } from '@/stores/credentials'
import { apiFetch } from '@/utils/api'
import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    component: LandingContainer,
    children: [
      { path: '', component: HeroSection },
      { path: 'features', component: FeaturesSection },
      { path: 'plans', component: PlansSection },
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
      { path: 'upload', name: 'upload', component: UploadTab },
      { path: 'customers', name: 'customers', component: CustomersTab },
      { path: 'model', name: 'model', component: ModelTab },
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
