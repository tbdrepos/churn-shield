<script lang="ts" setup>
import { ref } from 'vue'
import { apiFetch } from '@/utils/api'
import { useToastStore } from '@/stores/toastStore'

const toast = useToastStore()

const metrics = ref(null)
const charts = ref(null)
const loading = ref(false)

const loadInsights = async (id: string) => {
  loading.value = true
  try {
    metrics.value = await apiFetch(`/insights/model/metrics/${id}`)
    charts.value = await apiFetch(`/insights/model/charts/${id}`)
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
</script>
<template><div class=""></div></template>
<style lang="css" scoped></style>
