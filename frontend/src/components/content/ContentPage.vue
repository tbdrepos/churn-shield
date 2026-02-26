<script lang="ts" setup>
import ContentSidebar from './ContentSidebar.vue'
</script>

<template>
  <main>
    <ContentSidebar />
    <div class="content__container">
      <div class="container__header">
        Hello
        <!--TODO: put username here -->
      </div>
      <RouterView />
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
  padding: 2.5rem;
  background-color: var(--surface-2-color);
}
@media (width >= 48rem) {
  .content__container {
    margin-left: 250px;
  }
}
</style>
