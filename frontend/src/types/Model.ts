// types and schemas
export enum ModelStatus {
  training = 'training',
  trained = 'trained',
  failed = 'failed',
}

export interface Model {
  id: string
  name: string
  dataset_id: string
  dataset_name: string
  accuracy: number
  status: ModelStatus
  trained_at: Date
}

export interface ModelMetrics {
  accuracy: number
  precision: number
  recall: number
  f1_score: number
  roc_auc: number
}

export interface ModelIcon {
  key: string
  label: string
  value: string | number | null
  icon: string
  iconColor: string
}
