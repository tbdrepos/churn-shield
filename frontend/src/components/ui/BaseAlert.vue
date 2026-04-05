<script setup lang="ts">
defineProps<{
  message: string
  type?: 'error' | 'success' | 'warning' | 'info'
}>()
</script>

<template>
  <Transition name="fade">
    <div v-if="message" :class="['alert', `alert--${type || 'error'}`]" role="alert">
      <span class="alert-icon">⚠️</span> <span class="alert-text">{{ message }}</span>
    </div>
  </Transition>
</template>

<style scoped>
.alert {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  padding: 0.8rem 1rem;
  border-radius: 0.4rem;
  margin: 1rem 0;
  font-size: 0.9rem;
}
.alert--error {
  background-color: var(--color-danger);
  color: white;
  font-weight: 600;
}
/* Define --success-light etc. in your CSS variables */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
