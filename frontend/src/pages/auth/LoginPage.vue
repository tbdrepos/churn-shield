<script setup lang="ts">
import { ref } from 'vue'
import type { Token } from '@/types/auth'
import { useAuthStore } from '@/stores/authStore'
import { useRouter } from 'vue-router'
import { ApiError, apiFetch } from '@/utils/api'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
const router = useRouter()

const warning = ref({
  active: false,
  message: '',
})

const email = ref('')
const password = ref('')
const remember = ref(false)
const isLoggingIn = ref(false)

const resetWarning = () => {
  warning.value.active = false
}

async function requestLogin(): Promise<Token | undefined> {
  const formData = new FormData()
  formData.append('username', email.value)
  formData.append('password', password.value)

  return await apiFetch<Token>(`/auth/login?remember_me=${remember.value}`, {
    method: 'POST',
    body: formData,
  })
}

const loginUser = async () => {
  if (!email.value || !password.value) {
    warning.value.active = true
    warning.value.message = t('register.empty')
    return
  }

  try {
    isLoggingIn.value = true
    resetWarning() // Clear previous errors on new attempt

    const token = await requestLogin()
    if (token) {
      const auth = useAuthStore()
      auth.login(token.access_token, token.display_name)
      router.replace('/app')
    }
  } catch (err) {
    warning.value.active = true

    if (err instanceof ApiError) {
      if (err.status === 401) {
        warning.value.message = t('login.incorrect')
      } else if (err.status === 0) {
        // This handles the "NetworkError"
        warning.value.message =
          t('errors.network') || 'Network error. Please check your connection.'
      } else {
        warning.value.message =
          t('errors.server') || 'A server error occurred. Please try again later.'
      }
    } else {
      warning.value.message = t('errors.unexpected') || 'An unexpected error occurred.'
      console.error('Unexpected error:', err)
    }
  } finally {
    // Re-enable the form regardless of success or failure
    isLoggingIn.value = false
  }
}
</script>

<template>
  <div class="page__container">
    <div class="form__container">
      <h2>{{ t('login.title') }}</h2>
      <form @submit.prevent="loginUser">
        <fieldset :disabled="isLoggingIn">
          <input
            v-model="email"
            @input="resetWarning"
            autocomplete="email"
            name="email"
            type="email"
            :placeholder="t('login.email')"
            class="text__input"
          />
          <input
            v-model="password"
            @input="resetWarning"
            autocomplete="current-password"
            name="password"
            type="password"
            :placeholder="t('login.password')"
            class="text__input"
          />
          <div class="checkbox__container">
            <input v-model="remember" type="checkbox" name="remember" id="remember" />
            <label for="remember">{{ t('login.remember') }}</label>
          </div>

          <button type="submit" class="generic-button">
            {{ isLoggingIn ? t('login.processing') : t('login.action') }}
          </button>
        </fieldset>

        <div class="warning-message" v-if="warning.active">
          {{ warning.message }}
        </div>
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
fieldset {
  border: none;
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
.warning-message {
  color: var(--error-color);
  margin: 0;
  height: 1rem;
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
