<script setup lang="ts">
const model = defineModel<boolean>()
defineProps<{ label: string }>()

// Generate a random ID so the label and input always stay linked
const id = `checkbox-${Math.random().toString(36).slice(2, 9)}`
</script>

<template>
  <div class="checkbox-group">
    <input :id="id" v-model="model" type="checkbox" class="checkbox-input" />
    <label :for="id" class="checkbox-label">{{ label }}</label>
  </div>
</template>

<style scoped>
.checkbox-group {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  cursor: pointer;
}
.checkbox-input {
  width: 1.1rem;
  height: 1.1rem;
  accent-color: var(--color-primary-600);
}
.checkbox-label {
  font-size: 0.9rem;
  user-select: none;
}
</style>
