<script setup lang="ts">
import { computed } from 'vue'
import ApexChart from 'vue3-apexcharts'

import { mapChart } from '@/utils/chartMapper'
import type { CompositeChart } from '@/types/charts'

const props = defineProps<{
  charts: CompositeChart
}>()

const chartSettings = computed(() => {
  const chartSettings = []
  for (const chart of props.charts.charts) {
    chartSettings.push({ id: crypto.randomUUID(), option: mapChart(chart) })
  }
  return chartSettings
})
</script>

<template>
  <div>
    <h3>{{ charts.title }}</h3>
    <p>{{ charts.description }}</p>
    <div v-if="charts" class="chart-container">
      <ApexChart
        v-for="setting in chartSettings"
        :key="setting.id"
        :type="setting.option.chart?.type"
        :options="setting.option"
        :series="setting.option.series"
        height="300"
      />
    </div>
  </div>
</template>

<style scoped>
.chart-container {
  display: flex;
  padding: 16px;
  border-radius: 12px;
  background-color: var(--color-main);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  border: 1px solid var(--gray-300);
  overflow: scroll;
}

.chart-title {
  font-size: 14px;
  margin-bottom: 10px;
}
h3 {
  color: var(--gray-900);
  font-size: 1rem;
  margin: 0;
}
p {
  font-size: 0.8rem;
  color: var(--gray-900);
}
</style>
