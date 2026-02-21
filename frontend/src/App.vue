<script setup lang="ts">
import NavBar from './components/landing/NavBar.vue'
</script>

<template>
  <main>
    <NavBar />
    <RouterView />
  </main>
</template>

<style scoped>
main {
  display: flex;
  flex-direction: column;
}
</style>
