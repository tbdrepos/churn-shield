<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import { ref, reactive, computed } from 'vue'
import { useAuthStore } from '@/stores/authStore'
import { useRouter } from 'vue-router'
import { ApiError } from '@/utils/api'
import AuthReminder from '@/components/ui/AuthReminder.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import BaseCheckbox from '@/components/ui/BaseCheckbox.vue'
import PasswordInput from '@/components/ui/PasswordInput.vue'
import BaseAlert from '@/components/ui/BaseAlert.vue'
import AuthInput from '@/components/shared/AuthInput.vue'

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
          <AuthInput
            v-model="form.name"
            :placeholder="t('register.username')"
            autocomplete="name"
            @focus-action="resetWarning"
          />

          <AuthInput
            v-model="form.email"
            type="email"
            :placeholder="t('register.email')"
            autocomplete="email"
            @focus-action="resetWarning"
          />

          <PasswordInput
            v-model="form.password"
            :placeholder="t('register.password')"
            autocomplete="current-password"
            @input="resetWarning"
          />

          <PasswordInput
            v-model="form.confirm"
            :placeholder="t('register.confirm')"
            autocomplete="current-password"
            @input="resetWarning"
          />

          <BaseCheckbox :label="t('register.remember')" v-model="form.remember"></BaseCheckbox>

          <BaseButton
            type="submit"
            :loading="isRegistering"
            :disabled="isFormInvalid"
            :stretch="true"
          >
            {{ t('register.action') }}
          </BaseButton>

          <BaseAlert :message="errorMessage" />
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
