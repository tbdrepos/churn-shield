// =========================================================
// BASE CHART
// =========================================================

export type ChartTypes =
  | 'categorical'
  | 'xy'
  | 'boxplot'
  | 'missing_values'
  | 'target_distribution'
  | 'correlation_matrix'
  | 'outliers'
  | 'feature_distribution'
  | 'feature_target_relationship'
  | 'dataset_schema'
  | 'feature_importance'
  | 'prediction_distribution'
  | 'roc_curve'
  | 'calibration_curve'
  | 'confusion_matrix'

export type RenderTypes = 'categorical' | 'xy' | 'matrix' | 'boxplot' | 'table' | 'composite'

export interface BaseChart {
  chart_type: ChartTypes
  title: string
  description?: string
  render_type: RenderTypes
  x_axis?: string
  y_axis?: string
  legend?: string[]
}

export interface CategoricalChart extends BaseChart {
  render_type: 'categorical'
  categories: string[]
  series: number[]
}
export interface CompositeChart extends BaseChart {
  render_type: 'composite'
  charts: BaseChart[]
}
