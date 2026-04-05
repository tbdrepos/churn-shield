<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import { ref, reactive, computed } from 'vue'
import { useAuthStore } from '@/stores/authStore'
import { useRouter } from 'vue-router'
import { ApiError } from '@/utils/api'
import BaseInput from '@/components/ui/BaseInput.vue'
import AuthReminder from '@/components/ui/AuthReminder.vue'

const { t } = useI18n()
const router = useRouter()
const auth = useAuthStore()

const form = reactive({
  name: '',
  email: '',
  password: '',
  confirm: '',
  remember: false,
})

const isRegistering = ref(false)
const errorMessage = ref('')

const isFormInvalid = computed(() => {
  return !form.name || !form.email || !form.password || form.password !== form.confirm
})

const resetWarning = () => {
  errorMessage.value = ''
}

const handleRegister = async () => {
  if (form.password !== form.confirm) {
    errorMessage.value = t('register.mismatch')
    return
  }

  try {
    isRegistering.value = true
    resetWarning()

    const success = await auth.registerRequest(
      {
        display_name: form.name,
        email: form.email,
        password: form.password,
      },
      form.remember,
    )

    if (success) router.replace('/app')
  } catch (err) {
    // 4. Centralized Error Mapping
    if (err instanceof ApiError) {
      const errorMap: Record<number, string> = {
        409: t('register.emailConflict'),
        0: t('errors.network'),
      }
      errorMessage.value = errorMap[err.status] || t('errors.server')
    } else {
      errorMessage.value = t('errors.unexpected')
    }
  } finally {
    isRegistering.value = false
  }
}
</script>

<template>
  <div class="page__container">
    <div class="form__container">
      <h2>{{ t('register.title') }}</h2>

      <form @submit.prevent="handleRegister">
        <fieldset :disabled="isRegistering">
          <BaseInput
            v-model="form.name"
            :placeholder="t('register.username')"
            autocomplete="name"
            @focus-action="resetWarning"
          />

          <BaseInput
            v-model="form.email"
            type="email"
            :placeholder="t('register.email')"
            autocomplete="email"
            @focus-action="resetWarning"
          />

          <BaseInput
            v-model="form.password"
            type="password"
            :placeholder="t('register.password')"
            autocomplete="new-password"
            @focus-action="resetWarning"
          />

          <BaseInput
            v-model="form.confirm"
            type="password"
            :placeholder="t('register.confirm')"
            autocomplete="new-password"
            @focus-action="resetWarning"
          />

          <div class="checkbox__container">
            <input v-model="form.remember" type="checkbox" id="remember" />
            <label for="remember">{{ t('register.remember') }}</label>
          </div>

          <button type="submit" class="btn-primary" :disabled="isFormInvalid || isRegistering">
            {{ isRegistering ? t('login.processing') : t('register.action') }}
          </button>

          <div class="warning-message" role="alert">{{ errorMessage }}</div>
        </fieldset>
      </form>
    </div>

    <AuthReminder :message="t('register.reminder')" :link-text="t('login.action')" to="/login" />
  </div>
</template>

<style scoped>
.page__container {
  align-self: center;
  margin: 5rem 0;
}
.form__container {
  display: flex;
  flex-direction: column;
  align-items: center;
}
fieldset {
  border: none;
  display: flex;
  flex-direction: column;
  width: 30rem;
  gap: 1rem;
}
.warning-message {
  color: var(--error-color);
  height: 1rem;
  font-size: 0.9rem;
}
</style>
