// =========================================================
// BASE INTERFACES
// =========================================================

import type { BaseChart, CategoricalChart } from '@/types/charts'

// =========================================================
// FEATURE IMPORTANCE
// =========================================================

export interface FeatureImportanceChart extends CategoricalChart {
  chart_type: 'feature_importance'
  series: number[]
}

// =========================================================
// PREDICTION DISTRIBUTION
// =========================================================

export interface PredictionDistributionChart extends CategoricalChart {
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

export interface RocCurveChart extends BaseChart {
  chart_type: 'roc_curve'
  series: RocSeries[]
  auc: number
}

// =========================================================
// CONFUSION MATRIX
// =========================================================

export interface ConfusionMatrixData {
  x: string // x-axis label
  y: number
  count: number // probability
}

export interface ConfusionMatrixSeries {
  name: string
  data: ConfusionMatrixData[]
}

export interface ConfusionMatrixChart extends BaseChart {
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

export interface CalibrationCurveChart extends BaseChart {
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
