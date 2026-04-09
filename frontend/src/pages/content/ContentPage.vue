<script lang="ts" setup>
import { useAuthStore } from '@/stores/authStore'
import ContentSidebar from '@/components/layout/ContentSidebar.vue'
import { useRouter } from 'vue-router'
import BaseButton from '@/components/ui/BaseButton.vue'
import { useDark } from '@vueuse/core'
import { ref } from 'vue'
import logoDark from '@/assets/logo-dark.png'
import logoLight from '@/assets/logo-light.png'

const authStore = useAuthStore()
const router = useRouter()
const isDark = useDark()

const isCollapsed = ref()

const logOut = () => {
  authStore.logout()
  router.replace('/')
}
</script>

<template>
  <ContentSidebar v-model="isCollapsed" />
  <main :class="['main-content', isCollapsed ? 'collapsed' : 'expanded']">
    <div class="container__header">
      <img :src="!isDark ? logoDark : logoLight" alt="Logo" class="logo" />

      <h2>{{ authStore.user }}</h2>
      <div>
        <BaseButton @click="logOut" :stretch="true">Log out</BaseButton>
      </div>
    </div>
    <div class="tab__container">
      <RouterView />
    </div>
  </main>
</template>

<style scoped>
.main-content {
  transition: margin-left 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  min-height: 100vh;
  padding: 0 2rem;
  background-color: var(--gray-100);
}
.expanded {
  margin-left: var(--sidebar-expanded);
}
.collapsed {
  margin-left: var(--sidebar-collapsed);
}
.container__header {
  display: flex;
  justify-content: space-between;
  align-items: center;

  border-bottom: 1px solid var(--gray-300);
}
@media (max-width: 768px) {
  .main-content {
    margin-left: 0 !important;
    width: 100%;
  }
}
</style>
