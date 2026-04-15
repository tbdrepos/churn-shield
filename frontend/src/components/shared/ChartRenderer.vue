<script setup lang="ts">
import { computed } from 'vue'
import ApexChart from 'vue3-apexcharts'

import type { ModelChart } from '@/types/apiCharts'
import { mapChart } from '@/utils/chartMapper'

const props = defineProps<{
  chart: ModelChart
}>()

const mapped = computed(() => mapChart(props.chart))
const series = computed(() => props.chart.series)
</script>

<template>
  <div class="chart-container">
    <h3 v-if="chart.title" class="chart-title">
      {{ chart.title }}
    </h3>
    <p v-if="chart.description">{{ chart.description }}</p>

    <ApexChart
      v-if="mapped && series"
      :type="mapped.chart?.type"
      :options="mapped"
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
