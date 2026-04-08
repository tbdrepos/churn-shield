<script setup lang="ts">
import { useToastStore } from '@/stores/toastStore'
import BaseToast from '@/components/ui/BaseToast.vue'

const toastStore = useToastStore()
</script>

<template>
  <Teleport to="body">
    <div class="toaster-container">
      <TransitionGroup name="list">
        <BaseToast
          v-for="toast in toastStore.toasts"
          :key="toast.id"
          v-bind="toast"
          @close="toastStore.removeToast"
        />
      </TransitionGroup>
    </div>
  </Teleport>
</template>

<style scoped>
.toaster-container {
  position: fixed;
  top: 6rem;
  right: 2rem;
  z-index: 9999;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  pointer-events: none;
  /* Allows clicking things 'behind' the empty container */
}

/* Animations */
.list-enter-active,
.list-leave-active {
  transition: all 0.4s ease;
}

.list-enter-from {
  opacity: 0;
  transform: translateX(30px);
}

.list-leave-to {
  opacity: 0;
  transform: scale(0.9);
}
</style>
