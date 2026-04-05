<script setup lang="ts">
const model = defineModel<string>()

defineProps<{
  label?: string
  type?: string
  placeholder?: string
}>()

const emit = defineEmits(['focus-action'])
</script>

<template>
  <div class="input-group">
    <label v-if="label" :for="$attrs.id as string">{{ label }}</label>
    <input
      v-model="model"
      :type="type || 'text'"
      :placeholder="placeholder"
      v-bind="$attrs"
      class="text__input"
      @input="emit('focus-action')"
    />
  </div>
</template>

<style scoped>
.input-group {
  display: flex;
  flex-direction: column;
  width: 100%;
}
.text__input {
  all: unset;
  background-color: var(--surface-2-color);
  padding: 0.8rem 1rem;
  border: 1px solid var(--gray-300);
  border-radius: 0.2rem;
  transition: border-color 0.2s;
}
.text__input:focus {
  border: 2px solid var(--gray-500);
}
</style>
