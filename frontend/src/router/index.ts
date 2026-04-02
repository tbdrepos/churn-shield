import { useAuthStore } from '@/stores/authStore'
import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    component: () => import('@/pages/landing/LandingPage.vue'),
    children: [
      {
        path: '',
        name: 'home',
        meta: { guestOnly: true },
        component: () => import('@/components/layout/HeroSection.vue'),
      },
      {
        path: 'login',
        name: 'login',
        component: () => import('@/pages/auth/LoginPage.vue'),
        meta: { guestOnly: true },
      },
      {
        path: 'register',
        name: 'register',
        component: () => import('@/pages/auth/RegisterPage.vue'),
        meta: { guestOnly: true },
      },
    ],
  },
  {
    path: '/app',
    name: 'app',
    component: () => import('@/pages/content/ContentPage.vue'),
    redirect: '/app/dashboard',
    meta: { requiresAuth: true },
    children: [
      {
        path: 'dashboard',
        name: 'dashboard',
        component: () => import('@/pages/content/tabs/DashboardTab.vue'),
      },
      {
        path: 'dataset',
        name: 'dataset-list',
        component: () => import('@/pages/content/tabs/DatasetTab.vue'),
      },
      {
        path: 'dataset/:id',
        name: 'dataset-details',
        component: () => import('@/pages/content/tabs/DatasetDetails.vue'),
      },
      {
        path: 'upload',
        name: 'upload',
        component: () => import('@/pages/content/tabs/UploadTab.vue'),
      },
      {
        path: 'models',
        name: 'models-list',
        component: () => import('@/pages/content/tabs/ModelsTab.vue'),
      },
      {
        path: 'models/:id',
        name: 'model-details',
        component: () => import('@/pages/content/tabs/ModelDetails.vue'),
      },
      {
        path: 'insight',
        name: 'active-model-insight',
        component: () => import('@/pages/content/tabs/InsightTab.vue'),
      },
      {
        path: 'predict',
        name: 'predict',
        component: () => import('@/pages/content/tabs/PredictTab.vue'),
      },
      {
        path: 'account',
        name: 'account',
        component: () => import('@/pages/content/tabs/AccountTab.vue'),
      },
    ],
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: routes,
})

router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()

  // 1. If a token exists but isn't verified yet, validate it.
  if (authStore.token && !authStore.isVerified) {
    try {
      await authStore.verifySession()
    } catch {
      // If the token was junk, verifySession() already called logout().
      // If the page requires auth, send to login.
      if (to.meta.requiresAuth) return next({ name: 'login' })
    }
  }

  // 2. Guard: Protected Routes
  // If the route requires auth and the user isn't authenticated, redirect.
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    return next({ name: 'login' })
  }

  // 3. Guard: Guest-only Routes
  // If user is authenticated and tries to access them, send to dashboard.
  if (to.meta.guestOnly && authStore.isAuthenticated) {
    return next({ name: 'dashboard' })
  }

  // 4. Fallback: Stay on current path
  next()
})

export default router
