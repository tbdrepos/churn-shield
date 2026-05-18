<script setup lang="ts">
import NavBar from '@/components/layout/NavBar.vue'
</script>

<template>
  <main>
    <NavBar />
    <RouterView />
  </main>
</template>

<style scoped>
main {
  background-color: var(--gray-100);
  min-height: 100vh;
}
</style>
