<script setup lang="ts">
import { reactive } from 'vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import BaseInput from '@/components/ui/BaseInput.vue'
import BaseSelect from '@/components/ui/BaseSelect.vue'
import { arrayToOption } from '@/utils/formatter'
import { type CustomerSchema, DATASET_SCHEMA } from '@/types/dataset'

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
      <BaseButton @click="() => console.log(customerSchema)">Predict</BaseButton>
    </div>
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
</style>
