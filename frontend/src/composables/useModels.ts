import { apiFetch } from '@/utils/api'
import { useQuery, useMutation, useQueryClient, useIsMutating } from '@tanstack/vue-query'
import type { Model } from '@/types/model'
import { useToastStore } from '@/stores/toastStore'

// 1. Query Key Factory for consistency
export const modelKeys = {
  all: ['models'] as const,
  detail: (id: string) => [...modelKeys.all, id] as const,
}

// 2. API Fetcher
async function fetchModels(): Promise<Model[]> {
  return await apiFetch<Model[]>('/model/trained/all')
}

export function useModels() {
  const queryClient = useQueryClient()
  const isMutating = useIsMutating()

  const toast = useToastStore()

  // 3. Query for fetching data
  const query = useQuery({
    queryKey: modelKeys.all,
    queryFn: fetchModels,
    refetchInterval: isMutating.value > 0 ? false : 5000,
    staleTime: 10000, // Consider data fresh for 10 seconds
  })

  // 4. Mutation for deleting data
  const deleteMutation = useMutation({
    mutationFn: (id: string) => apiFetch(`/model/${id}`, { method: 'DELETE' }),

    // Auto-refetch models after a successful delete
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: modelKeys.all })
      toast.addToast(`Deletion succeed`, 'success')
    },

    // Replaces the manual alert logic with a more robust error handler
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
