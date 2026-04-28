<script setup lang="ts">
import { computed, reactive, ref } from 'vue'
import { useConfirmDialog } from '@vueuse/core'
import { useAuthStore } from '@/stores/authStore'
import { useToastStore } from '@/stores/toastStore'
import { toDisplayPercentage } from '@/utils/formatter'

// Components
import BaseButton from '@/components/ui/BaseButton.vue'
import BaseIcon from '@/components/ui/BaseIcon.vue'
import BaseInput from '@/components/ui/BaseInput.vue'
import BaseSelect from '@/components/ui/BaseSelect.vue'
import PasswordInput from '@/components/ui/PasswordInput.vue'
import BaseConfirmDialog from '@/components/ui/BaseConfirmDialog.vue'

const authStore = useAuthStore()
const toast = useToastStore()

// State Management
const isSaving = ref(false)
const isUpdatingPassword = ref(false)

const mlModels = [
  { label: 'Random Forest', value: 'RandomForest' },
  { label: 'Gradient Boosting', value: 'GradientBoosting' },
  { label: 'Logistic Regression', value: 'LogisticRegression' },
]

// Initialize form with store values
const accountInfo = reactive({
  name: authStore.user?.display_name || '',
  email: authStore.user?.email || '',
  preferred_classifier: authStore.settings?.preferred_classifier || '',
  churn_threshold: authStore.settings?.churn_threshold || 0.5,
})

const newPassword = reactive({
  new: '',
  confirm: '',
})

const thresholdPercentage = computed(() => toDisplayPercentage(accountInfo.churn_threshold))

// Actions
const handleSaveChanges = async () => {
  isSaving.value = true
  try {
    await Promise.all([
      authStore.updateInfo({ display_name: accountInfo.name }),
      authStore.updateSettings({
        preferred_classifier: accountInfo.preferred_classifier,
        churn_threshold: accountInfo.churn_threshold,
      }),
    ])
    toast.addToast('Settings updated successfully', 'success')
  } catch (error) {
    toast.addToast('Failed to save changes', 'error')
    console.error(error)
  } finally {
    isSaving.value = false
  }
}

// Dialog Logic
const {
  isRevealed: isUpdateRevealed,
  reveal: revealUpdate,
  confirm: confirmUpdate,
  cancel: cancelUpdate,
} = useConfirmDialog()
const {
  isRevealed: isDeleteRevealed,
  reveal: revealDelete,
  confirm: confirmDelete,
  cancel: cancelDelete,
} = useConfirmDialog()

const handleUpdatePassword = async () => {
  if (!newPassword.new || newPassword.new !== newPassword.confirm) {
    return toast.addToast('Passwords do not match', 'error')
  }

  const { isCanceled } = await revealUpdate()
  if (isCanceled) return

  isUpdatingPassword.value = true
  try {
    await authStore.updateInfo({ password: newPassword.new })
    toast.addToast('Password updated successfully', 'success')
    newPassword.new = ''
    newPassword.confirm = ''
  } catch (e) {
    toast.addToast('Failed to update password', 'error')
    console.error(e)
  } finally {
    isUpdatingPassword.value = false
  }
}

const handleDeleteAccount = async () => {
  const { isCanceled } = await revealDelete()
  if (!isCanceled) {
    try {
      await authStore.deleteAccount()
    } catch (e) {
      toast.addToast('Could not delete account', 'error')
      console.error(e)
    }
  }
}
</script>

<template>
  <div class="settings-container">
    <header class="settings-header">
      <h1>Account Settings</h1>
      <p>Manage your account details and model preferences.</p>
    </header>

    <section class="account-card">
      <div class="card-header">
        <h2>Account Information</h2>
        <hr />
      </div>

      <form class="settings-form" @submit.prevent="handleSaveChanges">
        <div class="form-grid">
          <BaseInput label="Name" v-model="accountInfo.name" />

          <BaseInput
            label="Email Address"
            disabled
            v-model="accountInfo.email"
            tooltip="Email cannot be changed."
          />

          <BaseSelect
            label="ML Model Selection"
            :options="mlModels"
            v-model="accountInfo.preferred_classifier"
          />

          <div class="form-group">
            <div class="label-row">
              <label>Churn Threshold</label>
              <span class="threshold-value">{{ thresholdPercentage }}</span>
            </div>
            <input
              type="range"
              min="0.2"
              max="0.8"
              step="0.1"
              v-model.number="accountInfo.churn_threshold"
              class="range-input"
            />
          </div>
        </div>

        <div class="form-actions">
          <BaseButton type="submit" :loading="isSaving" variant="primary">
            Save Changes
          </BaseButton>
        </div>
      </form>
    </section>

    <section class="actions-card">
      <div class="card security-section">
        <h2><BaseIcon name="LockKeyhole" /> Change Password</h2>
        <form class="vertical-container" @submit.prevent="handleUpdatePassword">
          <PasswordInput placeholder="New Password" v-model="newPassword.new" />
          <PasswordInput placeholder="Confirm New Password" v-model="newPassword.confirm" />
          <BaseButton variant="warning" type="submit" :loading="isUpdatingPassword">
            Update Password
          </BaseButton>
        </form>
      </div>

      <div class="card delete-section">
        <h2 class="text-danger"><BaseIcon name="TriangleAlert" /> Danger Zone</h2>
        <p>Permanently delete your account and all associated data. This action is irreversible.</p>
        <BaseButton variant="danger" @click="handleDeleteAccount"> Delete Account </BaseButton>
      </div>
    </section>
  </div>

  <BaseConfirmDialog
    :reveal="isDeleteRevealed"
    variant="danger"
    title="Delete Account?"
    confirm-text="Delete Permanently"
    @confirm="confirmDelete"
    @cancel="cancelDelete"
  />

  <BaseConfirmDialog
    :reveal="isUpdateRevealed"
    variant="primary"
    title="Confirm Password Change?"
    @confirm="confirmUpdate"
    @cancel="cancelUpdate"
  />
</template>

<style scoped lang="css">
.settings-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 0 1rem;
  font-family:
    system-ui,
    -apple-system,
    sans-serif;
  color: var(--color-contrast);
}

.settings-header {
  margin-bottom: 2rem;
}

.settings-header h1 {
  font-size: 1.875rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
}

.settings-header p {
  color: var(--gray-500);
  font-size: 1rem;
}

/* Card Styling */
.account-card {
  background: var(--color-main);
  border: 1px solid var(--color-primary-200);
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  padding: 2rem;
}

.card-header h2 {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 1rem;
}

hr {
  border: 0;
  border-top: 1px solid var(--color-primary-200);
  margin: 1.5rem 0;
}

/* Form Layout */
.settings-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-grid {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.form-actions {
  margin-top: 1rem;
  display: flex;
  justify-content: flex-end;
}

/* Custom Range Input Styling */
.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.label-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.label-row label {
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--gray-900);
}

.threshold-value {
  font-weight: 600;
  color: var(--color-primary);
  background: var(--color-primary-200);
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 0.875rem;
}

.range-input {
  width: 100%;
  height: 6px;
  background: var(--color-primary-200);
  border-radius: 5px;
  outline: none;
  accent-color: var(--color-primary); /* Modern browser support */
  cursor: pointer;
}

.range-labels {
  display: flex;
  justify-content: space-between;
  font-size: 0.75rem;
  color: var(--gray-100);
  margin-top: -0.25rem;
}

/* Specific styling for the disabled input state */
:deep(input:disabled) {
  background-color: var(--gray-300);
  cursor: not-allowed;
  color: var(--gray-700);
}

.actions-card {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin: 2rem 0;
}
.action-card-label {
  background-color: var(--color-danger);
  color: var(--color-main);
  border-radius: 1.2rem;
  box-shadow: 0 1rem 1rem rgb(from var(--color-danger) r g b / 0.6);
  padding: 1rem;
  margin: 0;
}
</style>
