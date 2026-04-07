import type { ModelStatus } from '@/types/Model'

export const getStatusVariant = (status: ModelStatus) => {
  if (status === 'trained') return 'success'
  if (status === 'failed') return 'danger'
  return 'neutral'
}
