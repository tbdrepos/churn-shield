<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import BaseButton from '../ui/BaseButton.vue'
import BaseIcon from '../ui/BaseIcon.vue'

const { t } = useI18n()
</script>
<template>
  <section>
    <div class="hero">
      <h1 class="hero__title">{{ t('landing.heroTitle') }}</h1>
      <p class="hero__description">{{ t('landing.heroDescription') }}</p>
      <RouterLink to="register" v-slot="{ navigate }">
        <BaseButton @click="navigate" :stretch="false" variant="primary">
          {{ t('landing.heroButton') }}
          <BaseIcon name="ArrowRight" />
        </BaseButton>
      </RouterLink>
    </div>
    <img src="@\assets\dashboard.png" alt="hero image" />
  </section>
</template>
<style lang="css" scoped>
section {
  display: flex;
  justify-content: space-between;
  padding: 1rem 6rem;
  gap: 2rem;
  background-color: var(--color-primary-900);
}
.hero {
  display: flex;
  flex-direction: column;
  align-items: start;
  justify-content: center;
  color: var(--color-main);
}
.hero__title {
  font-family: var(--heading-font-stack);
}
.hero__description {
  margin-bottom: 3rem;
  width: 34rem;
}
img {
  border-radius: 1rem;
}
@media (width < 102rem) {
  section {
    padding: 2rem;
  }
  img {
    width: 40rem;
  }
}
@media (width < 80rem) {
  .hero {
    width: 100%;
    align-items: center;
    text-align: center;
  }
  img {
    display: none;
  }
}
@media (width < 36rem) {
  .hero__description {
    width: 100%;
  }
}
</style>
