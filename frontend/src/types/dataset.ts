export interface Dataset {
  id: string
  original_name: string
  row_count: number
  uploaded_at: string
}
export interface SchemaRow {
  name: string
  type: string
  values: string
}

export const schema: SchemaRow[] = [
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
