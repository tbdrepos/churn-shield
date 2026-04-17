<script setup lang="ts">
import { computed } from 'vue'
import ApexChart from 'vue3-apexcharts'

import { mapChart, type CommonChart } from '@/utils/chartMapper'

const props = defineProps<{
  chart: CommonChart
}>()

const mapped = computed(() => mapChart(props.chart))
const series = computed(() => props.chart.series)
</script>

<template>
  <div v-if="chart" class="chart-container">
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
  background-color: var(--color-main);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  border: 1px solid var(--gray-300);
}

.chart-title {
  font-size: 14px;
  margin-bottom: 10px;
}
</style>
