<script setup lang="ts">
defineProps({
  icon: Object,
  label: String,
  value: String,
})
</script>

<template>
  <div class="stat-card">
    <div class="icon-box">
      <component v-if="icon" :is="icon"></component>
    </div>
    <h2 class="value">{{ value }}</h2>
    <p class="label">{{ label }}</p>
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
