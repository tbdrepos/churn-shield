<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  type?: 'button' | 'submit' | 'reset'
  variant?: 'primary' | 'secondary' | 'danger' | 'success' | 'warning'
  loading?: boolean
  disabled?: boolean
  stretch: boolean
}

const props = withDefaults(defineProps<Props>(), {
  type: 'button',
  variant: 'primary',
  loading: false,
  disabled: false,
  stretch: false,
})

const bgColor = computed(() => `var(--color-${props.variant})`)
const textColor = computed(() => {
  let colorName: string

  switch (props.variant) {
    case 'secondary':
      colorName = '--color-primary'
      break
    case 'primary':
      colorName = '--color-white'
      break
    default:
      colorName = '--color-black'
  }

  return `var(${colorName})`
})
</script>

<template>
  <button
    :type="type"
    :disabled="disabled || loading"
    :class="['base-btn', { 'full-width': props.stretch }, { 'is-loading': loading }]"
    :style="{
      '--btn-bg': bgColor,
      '--btn-text': textColor,
    }"
  >
    <span v-if="loading" class="btn-content">
      <span class="spinner"></span>
      <slot name="loading-text">{{ $t('common.loading') }}</slot>
    </span>

    <span v-else class="btn-content">
      <slot />
    </span>
  </button>
</template>

<style scoped>
.base-btn {
  background-color: var(--btn-bg);
  color: var(--btn-text);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 1rem 2rem;
  height: fit-content;
  font-weight: 600;
  border-radius: 0.4rem;
  border: 1px solid var(--btn-text);
  cursor: pointer;
  min-width: fit-content;
  line-height: 1.2;
  transition: all 0.2s ease;
}
.full-width {
  width: 100% !important;
}

.base-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.base-btn:hover:not(:disabled) {
  background-color: color-mix(in srgb, var(--btn-bg), black 15%);
}

.spinner {
  width: 1rem;
  height: 1rem;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: var(--btn-text);
  animation: spin 0.8s linear infinite;
  margin-right: 0.5rem;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>
