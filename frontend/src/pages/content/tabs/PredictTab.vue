<script setup lang="ts">
import { computed, reactive, ref, type Ref } from 'vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import BaseInput from '@/components/ui/BaseInput.vue'
import BaseSelect from '@/components/ui/BaseSelect.vue'
import { arrayToOption, toDisplayPercentage } from '@/utils/formatter'
import { type CustomerSchema, DATASET_SCHEMA } from '@/types/dataset'
import { apiFetch } from '@/utils/api'
import type { PredictResponse } from '@/types/model'
import DataTable from '@/components/shared/DataTable.vue'
import BaseIcon from '@/components/ui/BaseIcon.vue'
import MetricsCard from '@/components/shared/MetricsCard.vue'
import { useToastStore } from '@/stores/toastStore'
import { useAuthStore } from '@/stores/authStore'

const toast = useToastStore()
const authStore = useAuthStore()

const customerSchema = reactive<CustomerSchema>({
  Gender: 'Male',
  Age: 20,
  TenureMonths: 0,
  ContractType: 'Month-to-Month',
  MonthlyCharges: 0,
  TotalCharges: 0,
  PaymentMethod: 'Credit Card',
  InternetService: 'DSL',
  SupportCalls: 0,
})

const predictResponse: Ref<null | PredictResponse> = ref(null)

const disablePredict = computed(() => {
  console.log(authStore.settings?.active_model)
  return !authStore.settings?.active_model
})

const handlePredict = async () => {
  try {
    predictResponse.value = await apiFetch<PredictResponse>('/models/predict', {
      method: 'POST',
      body: JSON.stringify(customerSchema),
      headers: {
        'Content-Type': 'application/json',
      },
    })
  } catch (e) {
    console.error(e)
    toast.addToast('Failed to predict', 'error')
  }
}

const featureImpactLabels = [
  { key: 'feature', label: 'Feature' },
  { key: 'value', label: 'Value' },
  { key: 'direction', label: 'Risk Direction' },
  { key: 'impact_label', label: 'Impact' },
]

const riskAssessment = (risk: number) => {
  if (risk > 0.6) {
    return 'High Risk'
  } else if (risk > 0.3) {
    return 'Medium Risk'
  } else {
    return 'Low Risk'
  }
}

const riskDisplay = (risk: string) => {
  switch (risk) {
    case 'High Risk':
      return { class: 'danger', icon: 'ShieldX' }
    case 'Medium Risk':
      return { class: 'warning', icon: 'ShieldAlert' }
    case 'Low Risk':
      return { class: 'success', icon: 'ShieldCheck' }
    default:
      return { class: 'neutral', icon: 'ShieldEllipsis' }
  }
}
</script>

<template>
  <div class="predict-fields">
    <div v-for="field in DATASET_SCHEMA.slice(1, -1)" :key="field.name">
      <BaseInput
        v-if="field.type === 'int' || field.type === 'float'"
        :id="field.name"
        v-model="customerSchema[field.name]"
        :placeholder="String(field.values)"
        :label="field.name"
        type="number"
        class="field number-input"
      />

      <BaseSelect
        v-else-if="field.type === 'enum' && Array.isArray(field.values)"
        v-model="customerSchema[field.name]"
        :placeholder="field.name"
        :label="field.name"
        :options="arrayToOption(field.values)"
        class="field"
      />
    </div>

    <div class="predict-btn">
      <BaseButton :disabled="disablePredict" @click="handlePredict">Predict</BaseButton>
    </div>
  </div>
  <div class="title-with-line" v-if="predictResponse">
    <h2>Prediction Result</h2>
    <hr />
  </div>
  <div class="prediction-result" v-if="predictResponse">
    <MetricsCard
      label="Churn prediction"
      :value="predictResponse.prediction === 'Yes' ? 'Will Churn' : 'Will Not Churn'"
      :icon="predictResponse.prediction === 'Yes' ? 'TrendingDown' : 'TrendingUp'"
      :label-top="true"
      :icon-color="`--color-${riskDisplay(riskAssessment(predictResponse.probability)).class}`"
      :class="riskDisplay(riskAssessment(predictResponse.probability)).class"
    />
    <MetricsCard
      :label="riskAssessment(predictResponse.probability)"
      :value="toDisplayPercentage(predictResponse.probability)"
      :icon="riskDisplay(riskAssessment(predictResponse.probability)).icon"
      :label-top="true"
      :icon-color="`--color-${riskDisplay(riskAssessment(predictResponse.probability)).class}`"
      :class="riskDisplay(riskAssessment(predictResponse.probability)).class"
    />
  </div>
  <div class="feature-impact" v-if="predictResponse?.feature_impact">
    <div class="title-with-line">
      <h2>Feature Impact</h2>
      <hr />
    </div>
    <DataTable :headers="featureImpactLabels" :items="predictResponse?.feature_impact">
      <template #cell(direction)="{ item }">
        <div :class="item.direction === 'increase' ? 'danger' : 'success'">
          <BaseIcon :name="item.direction === 'increase' ? 'CircleArrowUp' : 'CircleArrowDown'" />
          {{ item.direction === 'increase' ? 'Increase' : 'Decrease' }}
        </div>
      </template>

      <template #cell(impact_label)="{ item }">
        <div :class="riskDisplay(item.impact_label).class">
          <BaseIcon :name="riskDisplay(item.impact_label).icon" />
          {{ item.impact_label }}
        </div>
      </template>
    </DataTable>
  </div>
</template>

<style scoped>
.predict-fields {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 2rem;
  margin: 1rem;
}
.field {
  width: 30rem;
}

.predict-btn {
  display: flex;
  align-self: self-end;
}
.prediction-result {
  display: flex;
  justify-content: space-around;
}
.feature-impact {
  margin-bottom: 2rem;
}
.success {
  color: var(--color-success);
}
.danger {
  color: var(--color-danger);
}
.neutral {
  color: var(--gray-500);
}
.warning {
  color: var(--color-warning);
}
</style>
