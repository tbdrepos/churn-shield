<script setup lang="ts">
import { ref } from 'vue'
import AuthInput from '../shared/AuthInput.vue'

const model = defineModel<string>()
const isVisible = ref(false)

const toggleVisibility = () => (isVisible.value = !isVisible.value)
</script>

<template>
  <div class="password-wrapper">
    <AuthInput v-model="model" :type="isVisible ? 'text' : 'password'" v-bind="$attrs" />
    <button type="button" @click="toggleVisibility" class="toggle-btn">
      {{ isVisible ? '🔒' : '🔓' }}
    </button>
  </div>
</template>

<style scoped>
.password-wrapper {
  position: relative;
  width: 100%;
}
.toggle-btn {
  position: absolute;
  right: 1rem;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  cursor: pointer;
  opacity: 0.6;
  font-size: 1.2rem;
}
</style>
