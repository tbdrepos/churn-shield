// =========================================================
// BASE INTERFACES
// =========================================================

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

// =========================================================
// FEATURE IMPORTANCE
// =========================================================

export interface FeatureImportanceChart extends CategoricalChart<'feature_importance'> {
  chart_type: 'feature_importance'
  series: number[]
}

// =========================================================
// PREDICTION DISTRIBUTION
// =========================================================

export interface PredictionDistributionChart extends CategoricalChart<'prediction_distribution'> {
  chart_type: 'prediction_distribution'
  series: number[]
}

// =========================================================
// ROC CURVE
// =========================================================

export interface RocData {
  x: number // fpr
  y: number // tpr
}

export interface RocSeries {
  name: string
  data: RocData[]
}

export interface RocCurveChart extends BaseChart<'roc_curve'> {
  chart_type: 'roc_curve'
  series: RocSeries[]
  auc: number
}

// =========================================================
// CONFUSION MATRIX
// =========================================================

export interface ConfusionMatrixData {
  x: string // x-axis label
  y: number // probability
  count: number
}

export interface ConfusionMatrixSeries {
  name: string
  data: ConfusionMatrixData[]
}

export interface ConfusionMatrixChart extends BaseChart<'confusion_matrix'> {
  chart_type: 'confusion_matrix'
  series: ConfusionMatrixSeries[]
  labels: string[] // y-axis labels
}

// =========================================================
// CALIBRATION CURVE
// =========================================================

export interface CalibrationSeries {
  name: string
  data: [number, number][] // [[pred, true]]
}

export interface CalibrationCurveChart extends BaseChart<'calibration_curve'> {
  chart_type: 'calibration_curve'
  series: CalibrationSeries[]
}

// =========================================================
// DISCRIMINATED UNION
// =========================================================

export type ModelChart =
  | FeatureImportanceChart
  | PredictionDistributionChart
  | RocCurveChart
  | ConfusionMatrixChart
  | CalibrationCurveChart
