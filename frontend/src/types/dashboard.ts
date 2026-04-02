export interface DashboardStats {
  total_databases: number | null
  total_models: number | null
  highest_accuracy: number | null
  active_model: string | null
}

export const defaults: DashboardStats = {
  total_databases: 0,
  total_models: 0,
  highest_accuracy: null,
  active_model: 'None',
}
