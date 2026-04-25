<script setup lang="ts">
import BaseButton from '@/components/ui/BaseButton.vue'
import BaseIcon from '@/components/ui/BaseIcon.vue'
import BaseInput from '@/components/ui/BaseInput.vue'
import BaseSelect from '@/components/ui/BaseSelect.vue'
import PasswordInput from '@/components/ui/PasswordInput.vue'
import { useAuthStore } from '@/stores/authStore'
import { toDisplayPercentage } from '@/utils/formatter'
import { computed, reactive } from 'vue'

const authStore = useAuthStore()

const mlModels = [
  { label: 'Random Forest', value: 'RandomForest' },
  { label: 'Gradient Boosting', value: 'GradientBoosting' },
  { label: 'Logistic Regression', value: 'LogisticRegression' },
]

const accountInfo = reactive({
  name: authStore.user?.display_name,
  email: authStore.user?.email,
  mlModel: authStore.settings?.active_model_id,
  threshold: authStore.settings?.churn_threshold,
})

const thresholdPercentage = computed(() => toDisplayPercentage(accountInfo.threshold))

const handleSaveChanges = () => {
  console.log(accountInfo)
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
          <BaseInput label="Name" :placeholder="accountInfo.name" v-model="accountInfo.name" />

          <BaseInput
            label="Email Address"
            :placeholder="accountInfo.email"
            disabled
            v-model="accountInfo.email"
          />

          <BaseSelect
            label="ML Model Selection"
            :options="mlModels"
            v-model="accountInfo.mlModel"
          />

          <div class="form-group">
            <div class="label-row">
              <label for="threshold">Churn Threshold</label>
              <span class="threshold-value">{{ thresholdPercentage }}</span>
            </div>
            <input
              name="threshold"
              type="range"
              min="0.2"
              max="0.8"
              step="0.1"
              v-model.number="accountInfo.threshold"
              class="range-input"
            />
            <div class="range-labels">
              <span>0.2</span>
              <span>0.8</span>
            </div>
          </div>
        </div>

        <div class="form-actions">
          <BaseButton type="submit" variant="primary">Save Changes</BaseButton>
        </div>
      </form>
    </section>
    <section class="actions-card">
      <div class="password-change card">
        <h2>
          <BaseIcon name="LockKeyhole" :size="24" fill="var(--color-warning)" /> Change Password
        </h2>
        <form class="vertical-container">
          <PasswordInput label="New Password" />
          <PasswordInput label="Confirm Password" />
          <BaseButton variant="warning">Change Password</BaseButton>
        </form>
      </div>
      <div class="delete-account card">
        <h2>
          <BaseIcon name="TriangleAlert" :size="24" fill="var(--color-danger)" />
          Delete Account
        </h2>
        <p>Permanently delete your account and all associated data.</p>
        <BaseButton variant="danger">Delete Account</BaseButton>
      </div>
    </section>
  </div>
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
  gap: 2rem;
  margin: 2rem 0;
}
</style>
