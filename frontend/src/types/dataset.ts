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

export interface CustomerSchema {
  Gender: 'Male' | 'Female'
  Age: number
  TenureMonths: number
  ContractType: 'Month-to-Month' | 'One Year' | 'Two Year'
  MonthlyCharges: number
  TotalCharges: number
  PaymentMethod: 'Credit Card' | 'Bank Transfer' | 'Electronic Check' | 'Mailed Check'
  InternetService: 'DSL' | 'Fiber Optic' | 'None'
  SupportCalls: number
}

export interface SchemaRow {
  name: string
  type: string
  values: string | string[]
}
export const DATASET_SCHEMA: SchemaRow[] = [
  { name: 'CustomerID', type: 'string', values: 'unique identifier' },
  { name: 'Gender', type: 'enum', values: ['Male', 'Female'] },
  { name: 'Age', type: 'int', values: 'customer age' },
  { name: 'TenureMonths', type: 'int', values: 'month using this service' },
  { name: 'ContractType', type: 'enum', values: ['Month-to-Month', 'One Year', 'Two Year'] },
  { name: 'MonthlyCharges', type: 'float', values: `customer's monthly charges` },
  { name: 'TotalCharges', type: 'float', values: 'total charge during tenure' },
  {
    name: 'PaymentMethod',
    type: 'enum',
    values: ['Credit Card', 'Bank Transfer', 'Electronic Check', 'Mailed Check'],
  },
  { name: 'InternetService', type: 'enum', values: ['DSL', 'Fiber Optic', 'None'] },
  { name: 'SupportCalls', type: 'int', values: 'number of times customer called support' },
  { name: 'Churn', type: 'enum', values: ['Yes', 'No'] },
]
