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
  uploaded_at: Date
  status: DatasetStatus
}
export interface SchemaRow {
  name: string
  type: string
  values: string
}
export interface DatasetMetrics {
  row_count: number
  column_count: number

  missing_rows: number
  null_value_ratio: number
  duplicate_rows: number

  churn_rate: number
  avg_tenure: number
  avg_monthly_revenue_per_user?: number
}
export interface DatasetIcon {
  key: string
  label: string
  value: string | number | null
}
