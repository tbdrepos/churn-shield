<script lang="ts" setup>
import { useAuthStore } from '@/stores/authStore'
import ContentSidebar from '@/components/layout/ContentSidebar.vue'
import { useRouter } from 'vue-router'
import BaseButton from '@/components/ui/BaseButton.vue'

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
        <div>
          <BaseButton @click="logOut" :stretch="true">Log out</BaseButton>
        </div>
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
  flex: 1;
  min-height: 100%;
}
.content__container {
  display: flex;
  flex-direction: column;
  margin-left: 60px;
  flex: 1;
  background-color: var(--gray-100);
  min-height: 100%;
}
.container__header {
  display: flex;
  justify-content: space-around;
  align-items: center;
  background-color: var(--color-white);
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
