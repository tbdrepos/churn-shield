<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import { useDark } from '@vueuse/core'

const isDark = useDark()
const { t } = useI18n()
</script>
<template>
  <nav>
    <RouterLink to="/" class="nav__link">{{ t('landing.features') }}</RouterLink>
    <RouterLink to="/" class="nav__link">{{ t('landing.plans') }}</RouterLink>

    <RouterLink to="/">
      <img
        :src="isDark ? '@/assets/logo-dark.png' : '@/assets/logo-light.png'"
        alt="logo"
        class="logo"
      />
    </RouterLink>

    <RouterLink to="/register" class="auth__sign-up nav__link">{{
      t('landing.sign_up')
    }}</RouterLink>
    <RouterLink to="/login" class="auth__Log-in nav__link">{{ t('landing.log_in') }}</RouterLink>
  </nav>
</template>
<style lang="css" scoped>
nav {
  display: flex;
  justify-content: center;
  gap: 0.5rem;
}
.logo-img {
  height: 6rem;
}

.nav__link {
  color: var(--primary-hover-color);
  font-size: 1.2rem;
  padding: 0.5rem;
  border-radius: 0.3rem;
  height: fit-content;
  margin-top: auto;
}
.nav__link:hover {
  background-color: color-mix(in srgb, var(--primary-hover-color), transparent 80%);
}
@media (width >= 48rem) {
  .logo-img {
    height: 8rem;
  }
  nav {
    gap: 3rem;
  }
  .nav__link {
    font-size: 1.3rem;
    padding: 0.6rem 0.8rem;
  }
}
</style>
