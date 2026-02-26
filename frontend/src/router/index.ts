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
    children: [
      { path: 'dashboard', component: DashboardTab },
      { path: 'upload', component: UploadTab },
      { path: 'customers', component: CustomersTab },
      { path: 'model', component: ModelTab },
      { path: 'account', component: AccountTab },
    ],
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: routes,
})

export default router
