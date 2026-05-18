<script setup lang="ts">
import type { LucideProps } from '@lucide/vue'
import type { FunctionalComponent } from 'vue'

defineProps<{
  title: string
  description: string
  icon: FunctionalComponent<LucideProps>
}>()
</script>

<template>
  <div class="feature">
    <div class="icon">
      <component :is="icon"></component>
    </div>
    <div class="description">
      <h6>{{ title }}</h6>
      <p>{{ description }}</p>
    </div>
  </div>
</template>

<style scoped>
.feature {
  display: flex;
}
.icon {
  background-color: var(--color-primary-200);
  border-radius: 1rem;
  padding: 0.8rem;
  height: fit-content;
}
.description {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
  margin-left: 1rem;
}
.description h6 {
  font-size: 1.2rem;
  margin: 0;
  width: 16rem;
}
.description p {
  color: var(--gray-500);
  margin: 0;
  width: 12rem;
}
</style>
