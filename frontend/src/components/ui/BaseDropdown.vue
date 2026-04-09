<script setup lang="ts">
import { ref } from 'vue'
import { onClickOutside } from '@vueuse/core'

interface Props {
  align?: 'left' | 'right'
  width?: string
}

withDefaults(defineProps<Props>(), {
  align: 'right',
  width: '200px',
})

const isOpen = ref(false)
const dropdownRef = ref<HTMLElement | null>(null)

const toggle = () => (isOpen.value = !isOpen.value)
const close = () => (isOpen.value = false)

// Close menu when clicking outside
onClickOutside(dropdownRef, close)
</script>

<template>
  <div ref="dropdownRef" class="base-dropdown">
    <div class="trigger" @click="toggle">
      <slot name="trigger" :is-open="isOpen" />
    </div>

    <Transition name="slide-up">
      <div
        v-if="isOpen"
        class="menu"
        :class="[`align-${align}`]"
        :style="{ width: width }"
        @click="close"
      >
        <slot />
      </div>
    </Transition>
  </div>
</template>

<style scoped>
.base-dropdown {
  position: relative;
  display: inline-block;
}

.trigger {
  cursor: pointer;
}

.menu {
  position: absolute;
  top: calc(100% + 8px);
  background: var(--color-main);
  border: 1px solid var(--color-primary-200);
  border-radius: 8px;
  box-shadow:
    0 10px 15px -3px rgba(0, 0, 0, 0.1),
    0 4px 6px -2px rgba(0, 0, 0, 0.05);
  z-index: 50;
  padding: 0.5rem 0;
  overflow: hidden;
}

.align-right {
  right: 0;
}
.align-left {
  left: 0;
}

/* Animation */
.slide-up-enter-active,
.slide-up-leave-active {
  transition: all 0.2s ease-out;
}
.slide-up-enter-from {
  opacity: 0;
  transform: translateY(10px);
}
.slide-up-leave-to {
  opacity: 0;
  transform: translateY(5px);
}

/* Scoped styles for menu items (standard pattern) */
:deep(.dropdown-item) {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  width: 100%;
  padding: 0.6rem 1rem;
  border: none;
  background: none;
  color: var(--gray-500);
  font-size: 0.9rem;
  text-align: left;
  cursor: pointer;
  transition: background 0.15s;
}

:deep(.dropdown-item:hover) {
  background: var(--color-main);
  color: var(--color-primary);
}

:deep(.dropdown-divider) {
  height: 1px;
  background: var(--color-primary-200);
  margin: 0.5rem 0;
}
</style>
