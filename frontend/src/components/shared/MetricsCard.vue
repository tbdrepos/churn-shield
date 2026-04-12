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
      <component class="icon" v-if="props.icon" :is="props.icon"></component>
    </div>
    <div class="stat-box">
      <h2 class="value">{{ props.value }}</h2>
      <p class="label">{{ props.label }}</p>
    </div>
  </div>
</template>

<style lang="css" scoped>
.stat-card {
  background: var(--color-main);
  padding: 0.5rem;
  border-radius: 0.5rem;
  display: flex;
  align-items: center;
  border: 1px solid var(--gray-300);
}

.stat-card .icon-box {
  width: 1rem;
  height: 1rem;
  margin-right: 0.5rem;
}

.icon {
  height: 1rem;
  width: 1rem;
  fill: var(--color-primary-200);
  stroke: var(--color-primary);
}

.stat-card .stat-box {
  display: flex;
  flex-direction: column;
}

.stat-card .value {
  font-size: 1rem;
  font-weight: 500;
  display: block;
  margin: 0;
}

.stat-card .label {
  font-size: 0.8rem;
  font-weight: 500;
  color: var(--gray-500);
  margin: 0;
}
</style>
