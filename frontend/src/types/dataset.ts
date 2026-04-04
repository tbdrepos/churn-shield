export interface Dataset {
  id: string
  original_name: string
  row_count: number
  uploaded_at: string
  status: 'uploaded' | 'training' | 'trained' | 'failed'
}
export interface SchemaRow {
  name: string
  type: string
  values: string
}
