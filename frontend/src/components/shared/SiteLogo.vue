<script setup lang="ts">
import { Shield } from '@lucide/vue'

defineProps({
  isBlack: {
    type: Boolean,
  },
})
</script>
<template>
  <div class="logo">
    <Shield class="shield-icon" />
    <h1 :class="isBlack ? 'churn-word-black' : 'churn-word'">Churn</h1>
    <h1 class="shield-word">Shield</h1>
  </div>
</template>
<style lang="css" scoped>
.logo {
  all: unset;
  text-decoration: none;
  display: flex;
  align-items: center;
}
.shield-icon {
  height: 3rem;
  width: 3rem;
  stroke: var(--color-contrast);
  fill: var(--color-primary);
}
.churn-word {
  color: var(--color-contrast);
}
.churn-word-black {
  color: var(--color-main);
}

.shield-word {
  color: var(--color-primary);
}
</style>
