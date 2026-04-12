<script setup lang="ts">
import type { InsightTabs } from '@/types/ui'

const modelValue = defineModel()

defineProps<{ tabs: InsightTabs }>()
</script>
<template>
  <div class="tabs-container">
    <nav class="tabs-nav" role="tablist">
      <button
        v-for="tab in tabs"
        :key="tab.value"
        type="button"
        role="tab"
        :aria-selected="modelValue === tab.value"
        @click="modelValue = tab.value"
        :class="['tab-button', { active: modelValue === tab.value }]"
      >
        {{ tab.label }}
      </button>
    </nav>

    <div class="tab-content">
      <slot :name="modelValue"></slot>
    </div>
  </div>
</template>

<style lang="css" scoped>
.tabs-nav {
  display: inline-flex;
  background-color: var(--gray-100);
  padding: 4px;
  border-radius: 8px;
  border: 1px solid var(--color-primary-200);
  margin-bottom: 24px;
}

.tab-button {
  padding: 8px 24px;
  font-size: 14px;
  font-weight: 600;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  background: transparent;
  color: var(--gray-700);
  transition: all 0.2s ease;
  outline: none;
}

.tab-button:hover:not(.active) {
  background-color: var(--gray-100);
  color: var(--gray-900);
}

.tab-button.active {
  background-color: var(--color-primary);
  color: var(--color-main);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.tabs-content {
  width: 100%;
}
</style>
