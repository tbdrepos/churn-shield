// functions
import { apiFetch } from '@/utils/api'
import { ref, onMounted } from 'vue'
import type { Model } from '@/types/Model'

export function useModels() {
  const models = ref<Model[] | null>(null)
  const loading = ref<boolean>(true)
  const error = ref<Error | null>(null)

  // Fetch initial data
  const fetchModels = async () => {
    loading.value = true
    error.value = null
    try {
      models.value = await apiFetch<Model[]>('/model/trained/all')
    } catch (err) {
      error.value = err instanceof Error ? err : new Error('An unknown error occurred')
    } finally {
      loading.value = false
    }
  }

  const viewModel = (id: string) => {}

  const deleteModel = async (id: string) => {
    try {
      await apiFetch(`/model/${id}`, { method: 'DELETE' })
      if (models.value) {
        models.value = models.value.filter((m) => m.id !== id)
      }
      alert(`Model ${id} deleted successfully.`)
    } catch (err) {
      if (err instanceof Error) alert(`Delete failed: ${err.message}`)
      else alert('Unexpected error during deletion')
    }
  }

  // Load data automatically when the component using this is mounted
  onMounted(fetchModels)

  return {
    models,
    loading,
    error,
    viewModel,
    deleteModel,
    refetch: fetchModels,
  }
}
