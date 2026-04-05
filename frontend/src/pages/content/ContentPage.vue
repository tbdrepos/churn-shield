<script lang="ts" setup>
import { useAuthStore } from '@/stores/authStore'
import ContentSidebar from '@/components/layout/ContentSidebar.vue'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

const logOut = () => {
  authStore.logout()
  router.replace('/')
}
</script>

<template>
  <main>
    <ContentSidebar />
    <div class="content__container">
      <div class="container__header">
        <h2>{{ authStore.user }}</h2>
        <button class="generic-button log-out__btn" @click="logOut">Log out</button>
      </div>
      <div class="tab__container">
        <RouterView />
      </div>
    </div>
  </main>
</template>

<style scoped>
main {
  display: flex;
}
.content__container {
  display: flex;
  flex-direction: column;
  margin-left: 60px;
  flex-grow: 1;
}
.container__header {
  display: flex;
  justify-content: end;
  padding: 1rem;
  background-color: var(--surface-2-color);
}
.log-out__btn {
  background-color: var(--primary-soft-color);
  color: var(--background-color);
}
@media (width >= 48rem) {
  .content__container {
    margin-left: 250px;
  }
  .tab__container {
    margin: 1rem;
  }
}
</style>
