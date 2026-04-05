<script setup lang="ts">
defineProps<{
  message: string
  linkText: string
  to: string
}>()
</script>

<template>
  <p class="reminder-message">
    {{ message }}
    <RouterLink :to="to">{{ linkText }}</RouterLink>
  </p>
</template>

<style scoped>
.reminder-message {
  text-align: center;
  margin-top: 1.5rem;
}
a {
  color: var(--color-primary-600);
  font-weight: 800;
  text-decoration: none;
}
a:hover {
  text-decoration: underline;
  opacity: 0.9;
}
</style>
