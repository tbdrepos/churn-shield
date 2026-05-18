<script setup lang="ts">
import SiteLogo from '@/components/shared/SiteLogo.vue'
import BaseButton from '../ui/BaseButton.vue'
</script>
<template>
  <nav>
    <RouterLink to="/" class="logo-link">
      <SiteLogo :isBlack="true" />
    </RouterLink>
    <div class="actions">
      <RouterLink to="/login">
        <BaseButton variant="secondary">Log In</BaseButton>
      </RouterLink>
      <RouterLink to="/register">
        <BaseButton variant="primary">Register</BaseButton>
      </RouterLink>
    </div>
  </nav>
</template>
<style lang="css" scoped>
nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 6rem;
  background-color: var(--color-primary-900);
  border-bottom: 1px solid var(--color-primary-600);
}
.logo-link {
  text-decoration: none;
}
.actions {
  display: flex;
  gap: 2rem;
}
@media (width < 48rem) {
  nav {
    padding: 0;
  }
}
@media (width < 36rem) {
  nav {
    flex-direction: column;
    padding-bottom: 2rem;
  }
}
</style>
