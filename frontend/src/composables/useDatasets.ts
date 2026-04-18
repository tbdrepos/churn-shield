// constants
import { useToastStore } from '@/stores/toastStore'
import { type Dataset } from '@/types/dataset'

// functions
import { apiFetch } from '@/utils/api'
import { useQuery, useMutation, useQueryClient } from '@tanstack/vue-query'

async function fetchDatasets(): Promise<Dataset[]> {
  return await apiFetch<Dataset[]>('/datasets/all')
}

export function useDatasets() {
  const queryClient = useQueryClient()

  const toast = useToastStore()

  const query = useQuery({
    queryKey: ['datasets'],
    queryFn: fetchDatasets,
    refetchInterval: (query) => {
      const data = query.state.data
      if (!data) return 5000

      const hasActiveDataset = data?.some(
        (d: Dataset) => d.status === 'uploaded' || d.status === 'training',
      )

      return hasActiveDataset ? 3000 : false
    },
    refetchIntervalInBackground: true,
    staleTime: 10000,
  })

  const trainMutation = useMutation({
    mutationFn: (id: string) => apiFetch(`/models/train/${id}`, { method: 'POST' }),
    onSuccess: async () => {
      await queryClient.invalidateQueries({ queryKey: ['datasets'] })
      await queryClient.invalidateQueries({ queryKey: ['models'] })
      toast.addToast(`Model training started.`, 'info')
    },
    onError: (err) => {
      const message = err instanceof Error ? err.message : 'Unknown error'
      toast.addToast(`Training failed: ${message}`, 'error', 5000)
    },
  })

  const deleteMutation = useMutation({
    mutationFn: (id: string) => apiFetch(`/datasets/${id}`, { method: 'DELETE' }),

    onSuccess: async () => {
      await queryClient.invalidateQueries({ queryKey: ['datasets'] })
      await queryClient.invalidateQueries({ queryKey: ['models'] })

      toast.addToast(`Dataset and associated models deleted successfully.`, 'success', 5000)
    },
    onError: (err) => {
      const message = err instanceof Error ? err.message : 'Unknown error'
      toast.addToast(`Delete failed: ${message}`, 'error')
    },
  })

  return {
    datasets: query.data,
    loading: query.isLoading,
    isRefetching: query.isRefetching,
    error: query.error,

    trainDataset: trainMutation.mutate,
    isTraining: trainMutation.isPending,

    deleteDataset: deleteMutation.mutate,
    isDeleting: deleteMutation.isPending,
  }
}
