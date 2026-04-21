<script setup lang="ts">
import { computed, ref, type ComputedRef, type Ref } from 'vue'
import { apiFetch } from '@/utils/api'
import { useToastStore } from '@/stores/toastStore'
import type { DatasetIcon, DatasetMetrics } from '@/types/dataset'
import MetricsCard from '@/components/shared/MetricsCard.vue'
import { toDisplayPercentage } from '@/utils/formatter'
import type { DataChart } from '@/types/datasetCharts'
import ChartRenderer from '@/components/shared/ChartRenderer.vue'

const toast = useToastStore()

const metrics: Ref<DatasetMetrics | null> = ref(null)
const charts: Ref<Array<DataChart> | null> = ref(null)
const loading = ref(false)

const loadInsights = async (id: string) => {
  loading.value = true
  try {
    metrics.value = await apiFetch<DatasetMetrics>(`/insights/dataset/metrics/${id}`)
    charts.value = await apiFetch<Array<DataChart>>(`/insights/dataset/charts/${id}`)

    // save to file
    /* const blob = new Blob([JSON.stringify(charts.value, null, 2)], { type: 'application/json' })
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', 'data.json') // Set the filename
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url) */
    // save to file

    toast.addToast('Insights loaded successfully!', 'success')
  } catch (e) {
    toast.addToast('Failed to fetch insights', 'error')
    if (e instanceof Error) console.error(`Failed to fetch insights: ${e.message}`)
  } finally {
    loading.value = false
  }
}

defineExpose({
  loadInsights,
})

const datasetMetrics: ComputedRef<DatasetIcon[]> = computed(() => {
  return [
    {
      key: 'row_count',
      value: metrics.value?.row_count ?? null,
      label: 'Row Count',
    },
    {
      key: 'column_count',
      value: metrics.value?.column_count ?? null,
      label: 'Column Count',
    },
    {
      key: 'missing_rows',
      value: metrics.value?.missing_rows ?? null,
      label: 'Missing Rows',
    },
    {
      key: 'null_value_ratio',
      value: toDisplayPercentage(metrics.value?.null_value_ratio),
      label: 'Null Value Ratio',
    },
    {
      key: 'duplicate_rows',
      value: metrics.value?.duplicate_rows ?? null,
      label: 'Duplicate Rows',
    },
    {
      key: 'churn_rate',
      value: toDisplayPercentage(metrics.value?.churn_rate),
      label: 'Churn Rate',
    },
    {
      key: 'avg_tenure',
      value:
        metrics.value?.avg_tenure !== undefined
          ? `${metrics.value?.avg_tenure.toFixed(2)} months`
          : null,
      label: 'Average Tenure',
    },
    {
      key: 'avg_monthly_revenue_per_user',
      value:
        metrics.value?.avg_monthly_revenue_per_user !== undefined
          ? `$${metrics.value?.avg_monthly_revenue_per_user.toFixed(2)}`
          : null,
      label: 'Average Monthly Revenue Per User',
    },
  ]
})

const chartSettings: ComputedRef<Array<{ key: string; chart: DataChart; col: string }>> = computed(
  () => {
    return [
      {
        key: 'dataset_schema',
        chart: charts.value?.find((chart) => chart.chart_type === 'dataset_schema') as DataChart,
        col: 'col-12',
      },
      {
        key: 'missing_values',
        chart: charts.value?.find((chart) => chart.chart_type === 'missing_values') as DataChart,
        col: 'col-6',
      },
      {
        key: 'outliers',
        chart: charts.value?.find((chart) => chart.chart_type === 'outliers') as DataChart,
        col: 'col-6',
      },
      {
        key: 'target_distribution',
        chart: charts.value?.find(
          (chart) => chart.chart_type === 'target_distribution',
        ) as DataChart,
        col: 'col-4',
      },
      {
        key: 'correlation_matrix',
        chart: charts.value?.find(
          (chart) => chart.chart_type === 'correlation_matrix',
        ) as DataChart,
        col: 'col-8',
      },
      {
        key: 'feature_distribution',
        chart: charts.value?.find(
          (chart) => chart.chart_type === 'feature_distribution',
        ) as DataChart,
        col: 'col-12',
      },
      {
        key: 'feature_target_relationship',
        chart: charts.value?.find(
          (chart) => chart.chart_type === 'feature_target_relationship',
        ) as DataChart,
        col: 'col-12',
      },
    ]
  },
)
</script>

<template>
  <h2>Dataset Metrics</h2>
  <p v-if="loading" class="sub-text">Loading insights...</p>
  <p v-else-if="!metrics" class="sub-text">Analyze a dataset to view insights...</p>
  <div v-if="metrics" class="metrics-container">
    <MetricsCard
      v-for="metric in datasetMetrics"
      :key="metric.key"
      :label="metric.label"
      :value="metric.value"
      :label-top="true"
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
  flex-wrap: wrap;
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
