<script lang="ts" setup>
import { computed, ref, type ComputedRef, type Ref } from 'vue'
import { apiFetch } from '@/utils/api'
import { useToastStore } from '@/stores/toastStore'
import MetricsCard from '@/components/shared/MetricsCard.vue'
import type { ModelIcon, ModelMetrics } from '@/types/model'
import type { ModelChart } from '@/types/modelCharts'
import ChartRenderer from '@/components/shared/ChartRenderer.vue'

const toast = useToastStore()

const metrics: Ref<ModelMetrics | null> = ref(null)
const charts: Ref<Array<ModelChart> | null> = ref(null)
const loading = ref(false)

const loadInsights = async (id: string) => {
  loading.value = true
  try {
    metrics.value = await apiFetch<ModelMetrics>(`/insights/model/metrics/${id}`)
    charts.value = await apiFetch<Array<ModelChart>>(`/insights/model/charts/${id}`)
    /* const blob = new Blob([JSON.stringify(charts.value, null, 2)], { type: 'application/json' })

    // 3. Create a temporary download link
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', 'data.json') // Set the filename

    // 4. Trigger download and cleanup
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)*/

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

const chartSettings: ComputedRef<Array<{ key: string; chart: ModelChart; col: string }>> = computed(
  () => {
    return [
      {
        key: 'roc_curve',
        chart: charts.value?.find((chart) => chart.chart_type === 'roc_curve') as ModelChart,
        col: 'col-8',
      },
      {
        key: 'prediction_distribution',
        chart: charts.value?.find(
          (chart) => chart.chart_type === 'prediction_distribution',
        ) as ModelChart,
        col: 'col-4',
      },
      {
        key: 'feature_importance',
        chart: charts.value?.find(
          (chart) => chart.chart_type === 'feature_importance',
        ) as ModelChart,
        col: 'col-6',
      },
      {
        key: 'calibration_curve',
        chart: charts.value?.find(
          (chart) => chart.chart_type === 'calibration_curve',
        ) as ModelChart,
        col: 'col-6',
      },
      {
        key: 'confusion_matrix',
        chart: charts.value?.find((chart) => chart.chart_type === 'confusion_matrix') as ModelChart,
        col: 'col-12',
      },
    ]
  },
)
</script>
<template>
  <p v-if="loading" class="sub-text">Loading insights...</p>

  <p v-else-if="!metrics" class="sub-text">Analyze a model to view insights...</p>
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
  <div v-if="chartSettings" class="charts-container">
    <ChartRenderer
      v-for="setting in chartSettings"
      :key="setting.key"
      :chart="setting.chart"
      :class="setting.col"
    />
  </div>
</template>
<style lang="css" scoped>
.metrics-container {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
}
.charts-container {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: 1rem;

  margin-bottom: 2rem;
}
.col-12 {
  grid-column: span 12;
}
.col-8 {
  grid-column: span 8;
}
.col-6 {
  grid-column: span 6;
}
.col-4 {
  grid-column: span 4;
}
.col-3 {
  grid-column: span 3;
}
</style>
