<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import { ref } from 'vue'
import { useAuthStore } from '@/stores/credentials'
import { useRouter } from 'vue-router'
import type { UserCreate, Token } from '@/types/auth'
import { ApiError, apiFetch } from '@/utils/api'

const { t } = useI18n()
const router = useRouter()

const warning = ref({
  active: false,
  message: '',
})

const name = ref('')
const email = ref('')
const password = ref('')
const confirm = ref('')
const remember = ref(false)
const isRegistering = ref(false)

const resetWarning = () => {
  warning.value.active = false
}

async function requestRegistration(): Promise<Token | undefined> {
  const user: UserCreate = {
    display_name: name.value,
    email: email.value,
    password: password.value,
  }

  try {
    isRegistering.value = true
    const response = await apiFetch<Token>(`/auth/register?remember_me=${remember.value}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(user),
    })
    return response
  } catch (err) {
    warning.value.active = true

    if (err instanceof ApiError) {
      if (err.status === 409) {
        warning.value.message = t('register.emailConflict')
      } else if (err.status === 0) {
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
    isRegistering.value = false
  }
}

const registerUser = async () => {
  if (!name.value || !email.value || !password.value || !confirm.value) {
    warning.value.active = true
    warning.value.message = t('register.empty')
    return
  }
  if (password.value != confirm.value) {
    warning.value.active = true
    warning.value.message = t('register.mismatch')
    return
  }
  const token = await requestRegistration()
  if (token) {
    const auth = useAuthStore()
    auth.login(token.access_token, token.display_name)
    console.log(token.display_name)
    router.replace('/app')
  }
}
</script>
<template>
  <div class="page__container">
    <div class="form__container">
      <h2>{{ t('register.title') }}</h2>
      <form @submit.prevent="registerUser">
        <fieldset :disabled="isRegistering">
          <input
            v-model="name"
            @click="resetWarning"
            autocomplete="username"
            name="name"
            type="text"
            :placeholder="t('register.username')"
            class="text__input"
          />
          <input
            v-model="email"
            @click="resetWarning"
            autocomplete="email"
            name="email"
            type="email"
            :placeholder="t('register.email')"
            class="text__input"
          />
          <input
            v-model="password"
            @click="resetWarning"
            autocomplete="password"
            name="password"
            type="password"
            :placeholder="t('register.password')"
            class="text__input"
          />
          <input
            v-model="confirm"
            @click="resetWarning"
            autocomplete="new-password"
            name="confirm"
            type="password"
            :placeholder="t('register.confirm')"
            class="text__input"
          />
          <div class="checkbox__container">
            <input v-model="remember" type="checkbox" name="remember" id="remember" />
            <label for="remember">{{ t('register.remember') }}</label>
          </div>
          <button type="submit" class="generic-button">
            {{ isRegistering ? t('login.processing') : t('register.action') }}
          </button>
          <div class="warning-message">{{ warning.active ? warning.message : '' }}</div>
        </fieldset>
      </form>
    </div>
    <p class="reminder-message">
      {{ t('register.reminder') }}
      <RouterLink to="login">{{ t('login.action') }}</RouterLink>
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
  margin: 2rem 0 1rem 0;
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
form button {
  background-color: var(--button-color);
  width: auto;
  text-align: center;
  border-radius: 0.2rem;
  padding: 0.8rem;
}
.warning-message {
  color: var(--error-color);
  margin: 0;
  height: 1rem;
}
.reminder-message {
  text-align: center;
  margin: 0;
}
a {
  color: var(--info-color);
  font-weight: 800;
}
a:hover {
  opacity: 0.9;
}
</style>
