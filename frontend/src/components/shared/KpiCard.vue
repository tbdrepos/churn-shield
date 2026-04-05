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
  background: white;
  padding: 24px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  border: 1px solid var(--gray-100);
  box-shadow:
    rgba(0, 0, 0, 0.16) 0px 3px 6px,
    rgba(0, 0, 0, 0.23) 0px 3px 6px;
}

.stat-card .icon-box {
  width: 3rem;
  height: 3rem;
  margin-right: 1.6rem;
}

.icon {
  height: 3rem;
  width: 3rem;
  fill: var(--color-primary-200);
  stroke: var(--color-primary);
}

.stat-card .stat-box {
  display: flex;
  flex-direction: column;
}

.stat-card .value {
  font-size: 1.8rem;
  font-weight: 700;
  display: block;
  margin: 0;
}

.stat-card .label {
  font-size: 1.1rem;
  font-weight: 500;
  color: var(--gray-500);
  margin: 0;
}
</style>
