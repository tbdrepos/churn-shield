import { apiFetch } from '@/utils/api'
import { useQuery, useMutation, useQueryClient } from '@tanstack/vue-query'
import type { Model } from '@/types/model'
import { useToastStore } from '@/stores/toastStore'

// 1. Query Key Factory for consistency
export const modelKeys = {
  all: ['models'] as const,
  detail: (id: string) => [...modelKeys.all, id] as const,
}

// 2. API Fetcher
async function fetchModels(): Promise<Model[]> {
  return await apiFetch<Model[]>('/models/trained/all')
}

export function useModels() {
  const queryClient = useQueryClient()

  const toast = useToastStore()

  // 3. Query for fetching data
  const query = useQuery({
    queryKey: modelKeys.all,
    queryFn: fetchModels,
    refetchInterval: (query) => {
      const data = query.state.data
      if (!data) return 5000

      const hasActiveDataset = data?.some((d: Model) => d.status === 'training')

      return hasActiveDataset ? 3000 : false
    },
    staleTime: 10000, // Consider data fresh for 10 seconds
  })

  // 4. Mutation for deleting data
  const deleteMutation = useMutation({
    mutationFn: (id: string) => apiFetch(`/models/${id}`, { method: 'DELETE' }),

    // Auto-refetch models after a successful delete
    onSuccess: async () => {
      await queryClient.invalidateQueries({ queryKey: modelKeys.all })
      toast.addToast(`Deletion succeed`, 'success')
    },
    onError: (err) => {
      const message = err instanceof Error ? err.message : 'Unknown error'
      console.error(`Delete failed: ${message}`)
      toast.addToast(`Delete failed: ${message}`, 'error')
    },
  })

  return {
    // Data & States
    models: query.data,
    isLoading: query.isLoading,
    isRefetching: query.isRefetching,
    error: query.error,

    // Actions
    deleteModel: deleteMutation.mutate,
    isDeleting: deleteMutation.isPending,
    refetch: query.refetch,
  }
}
