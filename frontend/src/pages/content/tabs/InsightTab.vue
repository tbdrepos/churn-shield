<script setup lang="ts">
import { computed, ref } from 'vue'
import ContentTabs from '@/components/layout/ContentTabs.vue'
import BaseSelect from '@/components/ui/BaseSelect.vue'
import { useModels } from '@/composables/useModels'

// 1. Setup the data from your composable
const { models, isLoading } = useModels()

// 2. State for the selected value
const selectedModelId = ref('')

// 3. Transform models into options automatically using Computed
// This is reactive: if models.value changes, selectOptions updates instantly.
const selectOptions = computed(() => {
  if (!models.value) return []

  return models.value.map((m) => ({
    label: m.name,
    value: m.id,
  }))
})
</script>

<template>
  <div class="">
    <h1>Model Insight</h1>
    <BaseSelect
      v-if="!isLoading"
      v-model="selectedModelId"
      label="Filter by Status"
      :options="selectOptions"
    />
    <div v-else class="skeleton-loader">Loading models...</div>
    <ContentTabs />
  </div>
</template>

<style scoped></style>
