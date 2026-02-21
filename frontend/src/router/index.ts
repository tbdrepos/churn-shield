import LoginPage from '@/components/auth/LoginPage.vue'
import RegisterPage from '@/components/auth/RegisterPage.vue'
import FeaturesSection from '@/components/landing/FeaturesSection.vue'
import HeroSection from '@/components/landing/HeroSection.vue'
import PlansSection from '@/components/landing/PlansSection.vue'
import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/', component: HeroSection },
  { path: '/features', component: FeaturesSection },
  { path: '/plans', component: PlansSection },
  { path: '/login', component: LoginPage },
  { path: '/register', component: RegisterPage },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: routes,
})

export default router
