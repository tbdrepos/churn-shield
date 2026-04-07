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
