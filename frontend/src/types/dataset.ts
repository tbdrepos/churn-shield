export enum DatasetStatus {
  uploaded = 'uploaded',
  training = 'training',
  trained = 'trained',
  failed = 'failed',
}

export interface Dataset {
  id: string
  original_name: string
  row_count: number
  uploaded_at: string
  status: DatasetStatus
}
export interface SchemaRow {
  name: string
  type: string
  values: string
}
