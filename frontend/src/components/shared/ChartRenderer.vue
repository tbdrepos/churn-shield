<script setup lang="ts">
import { computed } from 'vue'
import ApexChart from 'vue3-apexcharts'

import type { ModelChart } from '@/types/apiCharts'
import { mapChart } from '@/utils/chartMapper'
import type { BarChartOptions, DonutChartOptions } from '@/types/apexCharts'
import type { ApexOptions } from 'apexcharts'

const props = defineProps<{
  chart: ModelChart
}>()

const mapped = computed(() => mapChart(props.chart))

const options = computed((): ApexOptions => {
  switch (props.chart.chart_type) {
    case 'feature_importance':
      return {
        chart: { type: 'bar' as const },
      }
    /* case 'feature_distribution':
      return {
        chart: { type: 'bar' as const },
        xaxis: { categories: (mapped.value as BarChartOptions).categories },
      } */

    case 'prediction_distribution':
      return {
        chart: { type: 'donut' as const },
        labels: (mapped.value as DonutChartOptions).labels,
      }

    case 'roc_curve':
      return {
        chart: { type: 'line' as const },
      }
    case 'calibration_curve':
      return {
        chart: { type: 'line' as const },
        xaxis: { type: 'numeric' },
      }

    case 'confusion_matrix':
      return {
        chart: { type: 'heatmap' as const },
      }

    default:
      throw new Error('Could not match chart type ')
  }
})

const series = computed(() => mapped.value.series)
</script>

<template>
  <div class="chart-container">
    <h3 v-if="chart.title" class="chart-title">
      {{ chart.title }}
    </h3>

    <ApexChart
      v-if="options"
      :type="options.chart?.type"
      :options="options"
      :series="series"
      height="300"
    />
  </div>
</template>

<style scoped>
.chart-container {
  padding: 16px;
  border-radius: 12px;
}

.chart-title {
  font-size: 14px;
  margin-bottom: 10px;
}
</style>
