<script lang="ts" setup>
import { computed, ref, type ComputedRef, type Ref } from 'vue'
import { apiFetch } from '@/utils/api'
import { useToastStore } from '@/stores/toastStore'
import MetricsCard from '@/components/shared/MetricsCard.vue'
import type { ModelIcon, ModelMetrics } from '@/types/model'

const toast = useToastStore()

const metrics: Ref<ModelMetrics | null> = ref(null)
const charts = ref(null)
const loading = ref(false)

const loadInsights = async (id: string) => {
  loading.value = true
  try {
    metrics.value = await apiFetch<ModelMetrics>(`/insights/model/metrics/${id}`)
    charts.value = await apiFetch(`/insights/model/charts/${id}`)

    toast.addToast('Insights loaded successfully!', 'success')
  } catch (e) {
    toast.addToast('Failed to fetch insights', 'error')
    if (e instanceof Error) console.error(`Failed to fetch insights: ${e.stack}`)
  } finally {
    loading.value = false
  }
}

defineExpose({
  loadInsights,
})

const modelMetrics: ComputedRef<ModelIcon[]> = computed(() => {
  return [
    {
      key: 'accuracy',
      value: metrics.value?.accuracy.toFixed(2) ?? null,
      icon: 'CircleCheckBig',
      label: 'Accuracy',
      iconColor: '--color-success',
    },
    {
      key: 'precision',
      value: metrics.value?.precision.toFixed(2) ?? null,
      icon: 'Trophy',
      label: 'Precision',
      iconColor: '--chart-1',
    },
    {
      key: 'recall',
      value: metrics.value?.recall.toFixed(2) ?? null,
      icon: 'Clock',
      label: 'Recall',
      iconColor: '--chart-2',
    },
    {
      key: 'f1_score',
      value: metrics.value?.f1_score.toFixed(2) ?? null,
      icon: 'Scale',
      label: 'F1 Score',
      iconColor: '--chart-3',
    },
    {
      key: 'roc_auc',
      value: metrics.value?.roc_auc.toFixed(2) ?? null,
      icon: 'ChartSpline',
      label: 'ROC AUC',
      iconColor: '--chart-4',
    },
  ]
})
</script>
<template>
  <h2>Model Metrics</h2>
  <div v-if="metrics" class="metrics-container">
    <MetricsCard
      v-for="metric in modelMetrics"
      :key="metric.key"
      :label="metric.label"
      :value="metric.value"
      :icon="metric.icon"
      :label-top="true"
      :icon-color="metric.iconColor"
    />
  </div>
</template>
<style lang="css" scoped>
.metrics-container {
  display: flex;
  gap: 1rem;
}
</style>
