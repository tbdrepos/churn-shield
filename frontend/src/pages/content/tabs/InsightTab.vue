<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import BaseTabs from '@/components/ui/BaseTabs.vue'
import BaseSelect from '@/components/ui/BaseSelect.vue'
import ModelDetails from '@/pages/content/tabs/ModelDetails.vue'
import DatasetDetails from '@/pages/content/tabs/DatasetDetails.vue'
import type { InsightTabs, SelectOption } from '@/types/ui'
import { apiFetch } from '@/utils/api'
import type { Model } from '@/types/model'
import type { Dataset } from '@/types/dataset'
import BaseButton from '@/components/ui/BaseButton.vue'
import { useToastStore } from '@/stores/toastStore'

const toast = useToastStore()

const currentTab = ref('model')

const selectedId = ref('')

const tabs: InsightTabs = {
  model: { label: 'Model Insights', value: 'model' },
  data: { label: 'Data Insights', value: 'data' },
}

const selectModelOptions = ref<Array<SelectOption>>([])
const selectDatesetOptions = ref<Array<SelectOption>>([])

onMounted(async () => {
  try {
    const models = await apiFetch<Array<Model>>('/models/trained/all')
    const datasets = await apiFetch<Array<Dataset>>('/datasets/all')
    selectModelOptions.value = models.map((model) => ({
      label: model.name,
      value: model.id,
    }))
    selectDatesetOptions.value = datasets.map((dataset) => ({
      label: dataset.original_name,
      value: dataset.id,
    }))
  } catch (e) {
    toast.addToast('Failed to fetch models or datasets', 'error')
    if (e instanceof Error) console.error(`Failed to fetch models or datasets: ${e.message}`)
  }
})

const selectOptions = computed(() => {
  return currentTab.value === 'model' ? selectModelOptions.value : selectDatesetOptions.value
})

const modelDetailsRef = ref<InstanceType<typeof ModelDetails> | null>(null)
const datasetDetailsRef = ref<InstanceType<typeof DatasetDetails> | null>(null)

const fetchInsights = async (id: string) => {
  if (!id) return toast.addToast('Please select a model or dataset', 'warning')

  // 2. Call the fetch method based on the active tab
  if (currentTab.value === 'model' && modelDetailsRef.value) {
    await modelDetailsRef.value.loadInsights(id)
  } else if (currentTab.value === 'data' && datasetDetailsRef.value) {
    await datasetDetailsRef.value.loadInsights(id)
  }
}
</script>
<template>
  <div class="dashboard-page">
    <h2>{{ currentTab === 'model' ? tabs.model.label : tabs.data.label }}</h2>
    <div class="target-selection">
      <div class="selection-options">
        <BaseSelect
          v-model="selectedId"
          :placeholder="`Select the ${currentTab}...`"
          :options="selectOptions"
        />
      </div>
      <BaseButton @click="fetchInsights(selectedId)">Analyze</BaseButton>
    </div>
    <BaseTabs v-model="currentTab" :tabs="tabs">
      <template #model>
        <ModelDetails ref="modelDetailsRef" />
      </template>
      <template #data>
        <DatasetDetails ref="datasetDetailsRef" />
      </template>
    </BaseTabs>
  </div>
</template>

<style scoped>
.target-selection {
  display: flex;
  gap: 2rem;
  margin: 1rem 0;
}
.selection-options {
  width: 35rem;
}
</style>
