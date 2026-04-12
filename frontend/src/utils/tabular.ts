import type { DatasetStatus } from '@/types/dataset'
import type { ModelStatus } from '@/types/model'

export const getStatusVariant = (status: ModelStatus | DatasetStatus) => {
  if (status === 'trained') return 'success'
  if (status === 'failed') return 'danger'
  return 'neutral'
}
