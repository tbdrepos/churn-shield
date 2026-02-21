<script setup lang="ts">
import { useI18n } from 'vue-i18n'
const { t } = useI18n()
</script>
<template>
  <div class="page__container">
    <div class="form__container">
      <h2>{{ t('login.title') }}</h2>
      <form @submit.prevent="">
        <input name="email" type="email" :placeholder="t('login.email')" class="text__input" />
        <input
          name="password"
          type="password"
          :placeholder="t('login.password')"
          class="text__input"
        />
        <div class="checkbox__container">
          <input type="checkbox" name="remember" id="remember" />
          <label for="remember">{{ t('login.remember') }}</label>
        </div>
        <button type="submit" class="generic-button">{{ t('login.action') }}</button>
      </form>
    </div>
    <p>
      {{ t('login.reminder') }}
      <RouterLink to="register">{{ t('register.action') }}</RouterLink>
    </p>
  </div>
</template>
<style lang="css" scoped>
.page__container {
  align-self: center;
  margin: 5rem 0;
}
.form__container {
  margin: 2rem 0;
}
.form__container h2 {
  margin-bottom: 2rem;
}
form {
  display: flex;
  flex-direction: column;
  justify-content: center;
  width: 30rem;
  gap: 1rem;
}
.text__input {
  all: unset;
  background-color: var(--surface-2-color);
  padding: 0.8rem 1rem;
  border: 1px solid var(--surface-color);
  border-radius: 0.2rem;
}
.checkbox__container {
  margin-bottom: 1rem;
}
form button {
  background-color: var(--button-color);
  width: auto;
  text-align: center;
  border-radius: 0.2rem;
  padding: 0.8rem;
}
.page__container p {
  text-align: center;
}
a {
  color: var(--info-color);
  font-weight: 800;
}
a:hover {
  opacity: 0.9;
}
</style>
