<script setup lang="ts">
import { computed } from 'vue'
import ApexChart from 'vue3-apexcharts'

import { mapChart } from '@/utils/chartMapper'
import CompositeRenderer from './CompositeRenderer.vue'
import DataTable from './DataTable.vue'
import { featureSchemaColumns, type DatasetSchemaChart } from '@/types/datasetCharts'
import { type BaseChart, type CompositeChart } from '@/types/charts'

const props = defineProps<{
  chart: BaseChart
}>()

const renderType = computed(() => {
  if (props.chart.render_type === 'composite') {
    return 'composite'
  } else if (props.chart.render_type === 'table') {
    return 'table'
  }
  return 'single'
})
const mapped = computed(() => mapChart(props.chart))
</script>

<template>
  <div v-if="chart" class="chart-container">
    <CompositeRenderer v-if="renderType === 'composite'" :charts="chart as CompositeChart" />
    <DataTable
      v-if="renderType === 'table'"
      :headers="featureSchemaColumns"
      :items="(chart as DatasetSchemaChart).rows"
    />
    <ApexChart
      v-if="renderType === 'single' && mapped"
      :type="mapped.chart?.type"
      :options="mapped"
      :series="mapped.series"
      height="300"
    />
  </div>
</template>

<style scoped>
.chart-container {
  padding: 16px;
  border-radius: 12px;
  background-color: var(--color-main);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  border: 1px solid var(--gray-300);
}

.chart-title {
  font-size: 14px;
  margin-bottom: 10px;
}
</style>
