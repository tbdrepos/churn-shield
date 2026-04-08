// constants
import { useToastStore } from '@/stores/toastStore'
import type { SchemaRow, Dataset } from '@/types/dataset'

export const DATASET_SCHEMA: SchemaRow[] = [
  { name: 'CustomerID', type: 'int', values: 'unique identifier' },
  { name: 'Gender', type: 'enum', values: 'Male / Female' },
  { name: 'Age', type: 'int', values: 'customer age' },
  { name: 'TenureMonths', type: 'int', values: 'month using this service' },
  { name: 'ContractType', type: 'enum', values: 'Month-to-Month / One Year / Two Year' },
  { name: 'MonthlyCharges', type: 'float', values: `customer's monthly charges` },
  { name: 'TotalCharges', type: 'float', values: 'total charge during tenure' },
  {
    name: 'PaymentMethod',
    type: 'enum',
    values: 'Credit Card / Bank Transfer / Electronic Check / Mailed Check',
  },
  { name: 'InternetService', type: 'enum', values: 'DSL / Fiber Optic / None' },
  { name: 'SupportCalls', type: 'int', values: 'number of times customer called support' },
  { name: 'Churn', type: 'enum', values: 'Yes / No' },
]

// functions
import { apiFetch } from '@/utils/api'
import { useQuery, useMutation, useQueryClient, useIsMutating } from '@tanstack/vue-query'

async function fetchDatasets(): Promise<Dataset[]> {
  return await apiFetch<Dataset[]>('/datasets/all')
}

export function useDatasets() {
  const queryClient = useQueryClient()
  const isMutating = useIsMutating()

  const toast = useToastStore()

  const query = useQuery({
    queryKey: ['datasets'],
    queryFn: fetchDatasets,
    refetchInterval: isMutating.value > 0 ? false : 5000,
    refetchIntervalInBackground: true,
    staleTime: 10000,
  })

  const trainMutation = useMutation({
    mutationFn: (id: string) => apiFetch(`/model/train/${id}`, { method: 'POST' }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['datasets'] })
      // We also invalidate models because a new model is being created
      queryClient.invalidateQueries({ queryKey: ['models'] })
      toast.addToast(`Model training started.`, 'success')
    },
    onError: (err) => {
      const message = err instanceof Error ? err.message : 'Unknown error'
      toast.addToast(`Training failed: ${message}`, 'error')
    },
  })

  const deleteMutation = useMutation({
    mutationFn: (id: string) => apiFetch(`/datasets/${id}`, { method: 'DELETE' }),

    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['datasets'] })
      queryClient.invalidateQueries({ queryKey: ['models'] })

      toast.addToast(`Dataset and associated models deleted successfully.`, 'success')
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
