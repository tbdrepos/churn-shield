// types and schemas

export interface Model {
  id: string
  name: string
  dataset_id: string
  dataset_name: string
  accuracy: number
  status: 'training' | 'trained' | 'failed'
  trained_at: Date
}
