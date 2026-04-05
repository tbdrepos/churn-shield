<script setup lang="ts">
import { ref, reactive, computed } from 'vue'
import { useAuthStore } from '@/stores/authStore'
import { useRouter } from 'vue-router'
import { ApiError } from '@/utils/api'
import { useI18n } from 'vue-i18n'
import BaseInput from '@/components/ui/BaseInput.vue'
import AuthReminder from '@/components/ui/AuthReminder.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import PasswordInput from '@/components/ui/PasswordInput.vue'
import BaseAlert from '@/components/ui/BaseAlert.vue'

const { t } = useI18n()
const router = useRouter()
const auth = useAuthStore()

const form = reactive({
  email: '',
  password: '',
  remember: false,
})

const isLoggingIn = ref(false)
const errorMessage = ref('')

const isFormInvalid = computed(() => !form.email || !form.password)

const resetWarning = () => {
  errorMessage.value = ''
}

const handleLogin = async () => {
  try {
    isLoggingIn.value = true
    resetWarning()

    await auth.loginRequest(form.email, form.password, form.remember)
    router.replace('/app')
  } catch (err) {
    if (err instanceof ApiError) {
      const errorMap: Record<number, string> = {
        401: t('login.incorrect'),
        0: t('errors.network'),
      }
      errorMessage.value = errorMap[err.status] || t('errors.server')
    } else {
      errorMessage.value = t('errors.unexpected')
    }
  } finally {
    isLoggingIn.value = false
  }
}
</script>

<template>
  <div class="page__container">
    <div class="form__container">
      <h2>{{ t('login.title') }}</h2>

      <form @submit.prevent="handleLogin">
        <fieldset :disabled="isLoggingIn">
          <BaseInput
            v-model="form.email"
            type="email"
            :placeholder="t('login.email')"
            autocomplete="email"
            @input="resetWarning"
          />

          <PasswordInput
            v-model="form.password"
            :placeholder="t('login.password')"
            autocomplete="current-password"
            @input="resetWarning"
          />

          <BaseCheckbox :label="t('login.remember')" v-model="form.remember" />

          <BaseButton
            type="submit"
            :loading="isLoggingIn"
            :disabled="isFormInvalid"
            :stretch="true"
          >
            {{ t('login.action') }}

            <template #loading-text>{{ t('login.processing') }}</template>
          </BaseButton>

          <BaseAlert :message="errorMessage" />
        </fieldset>
      </form>
    </div>

    <AuthReminder :message="t('login.reminder')" :link-text="t('register.action')" to="/register" />
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
.checkbox__container {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.warning-message {
  color: var(--error-color);
  height: 1rem;
  font-size: 0.9rem;
}
</style>
