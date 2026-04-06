export interface DashboardStats {
  dataset_count: number | null
  model_count: number | null
  highest_accuracy: number | null
  active_model: string | null
}

export const defaults: DashboardStats = {
  dataset_count: 0,
  model_count: 0,
  highest_accuracy: null,
  active_model: 'None',
}
