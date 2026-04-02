<script setup lang="ts">
import KpiCard from '@/components/shared/KpiCard.vue'
import { useI18n } from 'vue-i18n'
import { Box, Cpu, Database, ShieldCheck } from '@lucide/vue'
import { computed, ref, onMounted } from 'vue'
import type { ComputedRef } from 'vue'
import { defaults } from '@/types/dashboard'
import type { DashboardStats } from '@/types/dashboard'
import { toDisplayPercentage } from '@/utils/formatter'
import { apiFetch } from '@/utils/api'

const { t } = useI18n()

const error = ref(null)
const loading = ref(false)
const values = ref(null)

async function fetchMetrics(){
  loading.value = true
  try{
    values.value = await apiFetch<DashboardStats>('/')
  }
  catch{}
  finally{
    loading.value = false
  }
}

const stats: ComputedRef<DashboardStats> = computed(() => ({
  total_databases: values.value?.total_databases ?? 0,
  total_models: values.value?.total_models ?? 0,
  highest_accuracy: values.value?.highest_accuracy ?? null,
  active_model: values.value?.active_model ?? 'None'
}))

const kpiItems = computed(() => [
  {
    key: 'databases',
    labelKey: 'dashboard.datasetLabel',
    icon: Database,
    displayValue: loading.value ? '—' : stats.value.total_databases,
  },
  {
    key: 'models',
    labelKey: 'dashboard.modelLabel',
    icon: Box,
    displayValue: loading.value ? '—' : stats.value.total_models,
  },
  {
    key: 'accuracy',
    labelKey: 'dashboard.accuracyLabel',
    icon: ShieldCheck,
    displayValue: loading.value
      ? '—'
      : stats.value.highest_accuracy != null
        ? toDisplayPercentage(stats.value.highest_accuracy)
        : '0%',
  },
  {
    key: 'active',
    labelKey: 'dashboard.activeLabel',
    icon: Cpu,
    displayValue: loading.value ? '—' : (stats.value.active_model ?? 'None'),
  },
])
</script>

<template>
  <div class="dashboard-container">
    <div class="stats-grid" role="region" aria-label="Key performance indicators">
      <KpiCard
        v-for="item in kpiItems"
        :key="item.key"
        :label="t(item.labelKey)"
        :icon="item.icon"
        :value="item.displayValue"
      />
    </div>

    <div class="middle-grid">
      <div class="card recent-activity">...</div>
      <div class="card quick-actions">...</div>
    </div>

    <div class="card table-card">
      <h3>Recent Models</h3>
      <table>
        ...
      </table>
    </div>
  </div>
</template>

<style scoped></style>
