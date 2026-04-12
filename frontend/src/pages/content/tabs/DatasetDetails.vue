<script setup lang="ts">
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
    metrics.value = await apiFetch(`/insights/dataset/metrics/${id}`)
    charts.value = await apiFetch(`/insights/dataset/charts/${id}`)
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

<template>
  <h1>a</h1>
</template>

<style lang="css" scoped></style>
