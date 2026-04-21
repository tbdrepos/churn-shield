<script setup lang="ts">
import BaseIcon from '@/components/ui/BaseIcon.vue'

const props = withDefaults(
  defineProps<{
    icon?: string
    label: string
    value: string | number | null
    labelTop?: boolean
    iconColor?: string
  }>(),
  {
    labelTop: false,
    iconColor: '--color-primary',
  },
)
</script>

<template>
  <div class="stat-card">
    <div class="icon-box">
      <BaseIcon class="icon" v-if="props.icon" :name="props.icon"></BaseIcon>
    </div>
    <div :class="labelTop ? 'stat-box-reversed' : 'stat-box'">
      <h2 class="value">{{ props.value }}</h2>
      <p class="label">{{ props.label }}</p>
    </div>
  </div>
</template>

<style lang="css" scoped>
.stat-card {
  background: var(--color-main);
  padding: 1.6rem;
  border-radius: 1rem;
  display: flex;
  align-items: center;
  border: 1px solid var(--gray-300);
  width: 16rem;
}

.stat-card .icon-box {
  margin-right: 1.5rem;
}

.icon {
  height: 2rem;
  width: 2rem;
  fill: v-bind('`var(${props.iconColor})`');
  stroke: var(--color-main);
  background-color: v-bind('`var(${props.iconColor})`');
  border-radius: 50%;
  padding: 0.5rem;
}

.stat-card .stat-box {
  display: flex;
  flex-direction: column;
}
.stat-card .stat-box-reversed {
  display: flex;
  flex-direction: column-reverse;
}

.stat-card .value {
  font-size: 1.6rem;
  font-weight: 500;
  display: block;
  margin: 0;
}

.stat-card .label {
  font-size: 1.2rem;
  font-weight: 500;
  color: var(--gray-500);
  margin: 0;
}
</style>
