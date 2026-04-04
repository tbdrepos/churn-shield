<script setup lang="ts">
import type { FunctionalComponent } from 'vue'

const props = defineProps<{
  icon: FunctionalComponent
  label: string
  value: string | number | null
}>()
</script>

<template>
  <div class="stat-card">
    <div class="icon-box">
      <component v-if="props.icon" :is="props.icon"></component>
    </div>
    <h2 class="value">{{ props.value }}</h2>
    <p class="label">{{ props.label }}</p>
  </div>
</template>

<style lang="css" scoped>
.stat-card {
  background: white;
  padding: 24px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  border: 1px solid var(--border-color);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.02);
}

.stat-card .icon-box {
  width: 48px;
  height: 48px;
  margin-right: 16px;
}

.stat-card .value {
  font-size: 28px;
  font-weight: 700;
  display: block;
}

.stat-card .label {
  font-size: 14px;
  color: var(--text-muted);
}
</style>
