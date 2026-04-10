<script setup lang="ts">
import { computed } from 'vue'
import BaseIcon from '@/components/ui/BaseIcon.vue'
import type { SelectOption } from '@/types/ui'

interface Props {
  modelValue: string | number | null
  options: SelectOption[]
  label?: string
  placeholder?: string
  error?: string
  disabled?: boolean
}

const props = defineProps<Props>()
const emit = defineEmits(['update:modelValue'])

// Unique ID for accessibility
const uuid = Math.random().toString(36).slice(2, 9)

const internalValue = computed({
  get: () => props.modelValue,
  set: (val) => emit('update:modelValue', val),
})
</script>

<template>
  <div class="base-select-wrapper">
    <label v-if="label" :for="uuid" class="select-label">
      {{ label }}
    </label>

    <div class="input-container" :class="{ 'has-error': error, 'is-disabled': disabled }">
      <select :id="uuid" v-model="internalValue" class="native-select" :disabled="disabled">
        <option v-if="placeholder" value="" disabled selected>
          {{ placeholder }}
        </option>
        <option v-for="opt in options" :key="opt.value" :value="opt.value">
          {{ opt.label }}
        </option>
      </select>

      <div class="chevron-icon">
        <BaseIcon name="ChevronDown" :size="18" />
      </div>
    </div>

    <Transition name="fade">
      <span v-if="error" class="error-text">{{ error }}</span>
    </Transition>
  </div>
</template>

<style scoped>
.base-select-wrapper {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  width: 100%;
}

.select-label {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--gray-300);
}

.input-container {
  position: relative;
  display: flex;
  align-items: center;
  background: var(--color-main);
  border: 1px solid var(--color-primary-200);
  border-radius: 8px;
  transition: all 0.2s ease;
}

/* Custom Focus Ring */
.input-container:focus-within {
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(26, 115, 232, 0.15);
}

.native-select {
  width: 100%;
  padding: 0.75rem 2.5rem 0.75rem 1rem;
  font-size: 0.95rem;
  color: var(--gray-300);
  background: transparent;
  border: none;
  outline: none;
  cursor: pointer;
  appearance: none; /* Hide default arrow */
}

.native-select:disabled {
  cursor: not-allowed;
}

.chevron-icon {
  position: absolute;
  right: 1rem;
  pointer-events: none;
  color: var(--gray-300);
  display: flex;
  align-items: center;
}

/* Error States */
.has-error {
  border-color: var(--color-danger);
}
.error-text {
  font-size: 0.75rem;
  color: var(--color-danger);
}

.is-disabled {
  background-color: var(--color-main);
  opacity: 0.7;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
