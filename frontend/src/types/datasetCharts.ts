// =========================================================
// SHARED TYPES & ALIASES
// =========================================================

import type { BaseChart, CategoricalChart, CompositeChart } from '@/types/charts'

/** Annotated[float, Field(ge=0, le=1)] */
export type UnitInterval = number

/** Annotated[float, Field(ge=-1, le=1)] */
export type CorrelationInterval = number

// =========================================================
// 1. MISSING VALUES & 2. TARGET DISTRIBUTION
// =========================================================

export interface MissingValuesChart extends CategoricalChart {
  chart_type: 'missing_values'
  percentages: UnitInterval[]
}

export interface TargetDistributionChart extends CategoricalChart {
  chart_type: 'target_distribution'
  percentages: UnitInterval[]
}

// =========================================================
// 3. CORRELATION MATRIX
// =========================================================

export interface CorrelationCell {
  x: string // feature name (column)
  y: CorrelationInterval // correlation value [-1, 1]
}

export interface CorrelationSeries {
  name: string // feature name (row)
  data: CorrelationCell[]
}

export interface CorrelationMatrixChart extends BaseChart {
  chart_type: 'correlation_matrix'
  series: CorrelationSeries[]
  labels: string[]
}

// =========================================================
// 4. DATASET SCHEMA & 5. OUTLIERS
// =========================================================

export interface FeatureSchema {
  name: string
  dtype: string
  missing_count: number
  unique_count: number
}

export const featureSchemaColumns: { key: string; label: string; width?: string }[] = [
  { key: 'name', label: 'name' },
  { key: 'dtype', label: 'dtype' },
  { key: 'missing_count', label: 'missing_count' },
  { key: 'unique_count', label: 'unique_count' },
]

export interface DatasetSchemaChart extends BaseChart {
  chart_type: 'dataset_schema'
  render_type: 'table'
  rows: FeatureSchema[]
}

export interface BoxPlotChart extends BaseChart {
  chart_type: 'boxplot'
  render_type: 'boxplot'
  series: number[] // [lower, q1, median, q3, upper]
}

export interface OutliersChart extends CompositeChart {
  chart_type: 'outliers'
  charts: BoxPlotChart[]
}

// =========================================================
// 6. FEATURE ↔ TARGET & 7. FEATURE DISTRIBUTION
// =========================================================

export interface XYChart extends BaseChart {
  chart_type: 'xy'
  render_type: 'xy'
  series: number[][] // [[x1, y1], [x2, y2], ...]
}

export interface FeatureTargetRelationshipChart extends CompositeChart {
  chart_type: 'feature_target_relationship'
  charts: XYChart[]
}

export interface FeatureBarChart extends CategoricalChart {
  chart_type: 'categorical'
}

export interface FeatureDistributionChart extends CompositeChart {
  chart_type: 'feature_distribution'
  charts: FeatureBarChart[]
}

// =========================================================
// DISCRIMINATED UNION
// =========================================================

export type DataChart =
  | MissingValuesChart
  | CorrelationMatrixChart
  | TargetDistributionChart
  | FeatureTargetRelationshipChart
  | FeatureDistributionChart
  | OutliersChart
  | DatasetSchemaChart
  | FeatureBarChart
  | XYChart
  | BoxPlotChart
