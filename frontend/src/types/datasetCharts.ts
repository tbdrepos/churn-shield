export interface BaseChart<T extends string> {
  chart_type: T
  title: string
  description?: string
  x_axis?: string
  y_axis?: string
  legend?: string[]
}

export interface CategoricalChart<T extends string> extends BaseChart<T> {
  categories: string[]
}

export interface MissingValuesChart extends CategoricalChart<'missing_values'> {
  chart_type: 'missing_values'
  series: number[] // missing_counts
  percentages: number[]
}

export interface TargetDistributionChart extends CategoricalChart<'target_distribution'> {
  chart_type: 'target_distribution'
  series: number[] // counts
  percentages: number[]
}
export interface CorrelationCell {
  x: string // feature name
  y: number // correlation value: -1 ≤ y ≤ 1
}

export interface CorrelationSeries {
  name: string // feature name (row)
  data: CorrelationCell[]
}

export interface CorrelationMatrixChart extends BaseChart<'correlation_matrix'> {
  chart_type: 'correlation_matrix'
  series: CorrelationSeries[]
  labels: string[]
}

export interface OutlierStats {
  x: string // feature name
  y: number // [min,q1,median,q2, max]
}

export interface OutlierSeries {
  name: string
  data: OutlierStats[]
}

export interface OutliersChart extends BaseChart<'outliers'> {
  chart_type: 'outliers'
  series: OutlierSeries[]
}
export interface FeatureTargetRelationshipChart extends CategoricalChart<'feature_target_relationship'> {
  chart_type: 'feature_target_relationship'
  series: number[] // target_rate
}

export interface FeatureDistributionChart extends CategoricalChart<'feature_distribution'> {
  chart_type: 'feature_distribution'
  series: number[] // counts
}
export type DataChart =
  | MissingValuesChart
  | TargetDistributionChart
  | CorrelationMatrixChart
  | OutliersChart
  | FeatureTargetRelationshipChart
  | FeatureDistributionChart
