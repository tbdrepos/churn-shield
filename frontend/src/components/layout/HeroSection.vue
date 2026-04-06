<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import BaseButton from '../ui/BaseButton.vue'

const { t } = useI18n()
</script>
<template>
  <section>
    <div class="hero">
      <h1 class="hero__title">{{ t('landing.heroTitle') }}</h1>
      <p class="hero__description">{{ t('landing.heroDescription') }}</p>
      <RouterLink to="register" v-slot="{ navigate }">
        <BaseButton @click="navigate" :stretch="false" variant="primary">{{
          t('landing.heroButton')
        }}</BaseButton>
      </RouterLink>
    </div>
    <img src="@\assets\infographic07.jpg" alt="hero image" />
  </section>
</template>
<style lang="css" scoped>
section {
  display: flex;
  justify-content: center;
}
.hero {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  margin: 2rem;
}
.hero__title {
  font-family: var(--heading-font-stack);
}
.hero__description {
  margin-bottom: 3rem;
}
img {
  display: none;
}
@media (width >= 48rem) {
  .hero {
    justify-content: center;
  }
  img {
    display: block;
    border-radius: 2rem;
    height: 25rem;
    margin: 1rem;
    align-self: center;
  }
}
@media (width >= 64rem) {
  img {
    height: 30rem;
    margin: 3rem;
  }
}
@media (width >= 80rem) {
  section {
    gap: 4rem;
  }
  .hero {
    max-width: 30rem;
  }
}
</style>
