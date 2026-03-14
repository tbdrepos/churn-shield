<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import { ref } from 'vue'
import type { Token } from '@/types/auth'
import { useAuthStore } from '@/stores/credentials'
import { useRouter } from 'vue-router'
import { ApiError, apiFetch } from '@/utils/api'

const { t } = useI18n()

const router = useRouter()

const warning = ref({
  active: false,
  message: '',
})

const email = ref('')
const password = ref('')

const resetWarning = () => {
  warning.value.active = false
}

async function requestLogin(): Promise<Token | undefined> {
  const formData = new FormData()
  formData.append('username', email.value)
  formData.append('password', password.value)

  try {
    const tokenData = await apiFetch<Token>('/auth/login', {
      method: 'POST',
      body: formData,
    })
    /* const response = await fetch('http://127.0.0.1:8000/api/v1/auth/login', {
      method: 'POST',
      body: formData,
    })
    const tokenData = (await response.json()) as Token */
    return tokenData
  } catch (err) {
    if (err instanceof ApiError) {
      console.error(`API error ${err.status}: ${err.message}`)
    } else {
      console.error('Unexpected error:', err)
    }
  }
}

const loginUser = async () => {
  if (!email.value || !password.value) {
    warning.value.active = true
    warning.value.message = t('register.empty')
    return
  }
  const token = await requestLogin()
  if (token) {
    const auth = useAuthStore()
    auth.login(token.access_token, token.display_name)
    router.replace('/app')
  }
}
</script>
<template>
  <div class="page__container">
    <div class="form__container">
      <h2>{{ t('login.title') }}</h2>
      <form @submit.prevent="loginUser">
        <input
          v-model="email"
          @click="resetWarning"
          autocomplete="email"
          name="email"
          type="email"
          :placeholder="t('login.email')"
          class="text__input"
        />
        <input
          v-model="password"
          @click="resetWarning"
          autocomplete="password"
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
  display: flex;
  flex-direction: column;
  align-items: center;
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
