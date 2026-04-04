import { computed, ref, onMounted } from 'vue'
import type { ComputedRef, Ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { Box, Cpu, Database, ShieldCheck } from '@lucide/vue'
import { defaults } from '@/types/dashboard'
import type { DashboardStats } from '@/types/dashboard'
import { toDisplayPercentage } from '@/utils/formatter'
import { apiFetch } from '@/utils/api'
import type { Dataset } from '@/types/dataset'
import type { Model } from '@/types/Model'

export function useDashboard() {
  const { t } = useI18n()

  // --- State ---
  const error: Ref<Error | null> = ref(null)
  const loading: Ref<boolean> = ref(false)
  const statValues: Ref<DashboardStats | null> = ref(null)
  const recentActivity: Ref<Array<string> | null> = ref(null)
  const recentModels: Ref<Array<Model> | null> = ref(null)

  // --- Actions ---
  async function fetchMetrics() {
    loading.value = true
    error.value = null
    try {
      const [stats, activity, models] = await Promise.all([
        apiFetch<DashboardStats>('/summary'),
        apiFetch<Array<string>>('/summary/activity'),
        apiFetch<Array<Model>>('/summary/models'),
      ])

      statValues.value = stats
      recentActivity.value = activity
      recentModels.value = models
    } catch (err) {
      if (err instanceof Error) error.value = err
      console.error('Failed to fetch dashboard metrics:', err)
      statValues.value = defaults
    } finally {
      loading.value = false
    }
  }

  // --- Computed ---
  const stats = computed(() => ({
    total_databases: statValues.value?.total_databases ?? 0,
    total_models: statValues.value?.total_models ?? 0,
    highest_accuracy: statValues.value?.highest_accuracy ?? null,
    active_model: statValues.value?.active_model ?? 'None',
    recent_activity: recentActivity.value ?? [],
    recent_models: recentModels.value ?? [],
  }))

  const kpiItems = computed(() => [
    {
      key: 'databases',
      label: t('dashboard.datasetLabel'),
      icon: Database,
      displayValue: loading.value ? '—' : stats.value.total_databases,
    },
    {
      key: 'models',
      label: t('dashboard.modelLabel'),
      icon: Box,
      displayValue: loading.value ? '—' : stats.value.total_models,
    },
    {
      key: 'accuracy',
      label: t('dashboard.accuracyLabel'),
      icon: ShieldCheck,
      displayValue: loading.value
        ? '—'
        : stats.value.highest_accuracy != null
          ? toDisplayPercentage(stats.value.highest_accuracy)
          : '0%',
    },
    {
      key: 'active',
      label: t('dashboard.activeLabel'),
      icon: Cpu,
      displayValue: loading.value ? '—' : (stats.value.active_model ?? 'None'),
    },
  ])

  // --- Lifecycle ---
  onMounted(fetchMetrics)

  return {
    loading,
    error,
    stats,
    kpiItems,
    fetchMetrics,
  }
}
