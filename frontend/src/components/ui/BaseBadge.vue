<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  variant?: 'success' | 'danger' | 'warning' | 'neutral'
}>()

const classes = computed(() => ['base-badge', `base-badge--${props.variant || 'neutral'}`])
</script>

<template>
  <span :class="classes">
    <slot />
  </span>
</template>

<style scoped>
.base-badge {
  display: inline-flex;
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.85rem;
  font-weight: 500;
  text-transform: capitalize;
}

.base-badge--success {
  background-color: #e6f4ea;
  color: var(--color-success);
}
.base-badge--danger {
  background-color: #fce8e8;
  color: var(--color-danger);
}
.base-badge--warning {
  background-color: #fef7e0;
  color: var(--color-warning);
}
.base-badge--neutral {
  background-color: #f1f3f4;
  color: var(--gray-300);
}
</style>
