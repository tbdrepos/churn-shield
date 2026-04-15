import * as ChartTypes from '@/types/apiCharts'
import type { ApexOptions } from 'apexcharts'

// Feature Importance → Bar Chart
export function mapFeatureImportance(modelChart: ChartTypes.ModelChart): ApexOptions {
  const chart = modelChart as ChartTypes.FeatureImportanceChart
  return {
    chart: { type: 'bar' },
    title: { text: chart.title },
    xaxis: {
      categories: chart.categories || [],
      title: { text: chart.x_axis },
      labels: {
        // value is the raw data point
        formatter: (value) => {
          if (typeof value === 'number') return value.toFixed(2)
          return value // Return as-is if it's a category string
        },
      },
    },
    yaxis: {
      title: { text: chart.y_axis },
      labels: {
        // value is the raw data point
        formatter: (value) => {
          if (typeof value === 'number') return value.toFixed(2)
          return value // Return as-is if it's a category string
        },
      },
    },
    labels: chart.legend || [],
    plotOptions: {
      bar: {
        horizontal: true,
      },
    },
  }
}

// Prediction Distribution → Donut
export function mapPredictionDistribution(modelChart: ChartTypes.ModelChart): ApexOptions {
  const chart = modelChart as ChartTypes.PredictionDistributionChart
  return {
    chart: { type: 'pie' },
    title: { text: chart.title },
    labels: chart.categories || [],
  }
}

// Confusion Matrix → Heatmap
export function mapConfusionMatrix(modelChart: ChartTypes.ModelChart): ApexOptions {
  const chart = modelChart as ChartTypes.ConfusionMatrixChart
  return {
    chart: { type: 'heatmap' },
    title: { text: chart.title },
    labels: chart.labels || [],
  }
}

// ROC Curve → Line
export function mapRocCurve(modelChart: ChartTypes.ModelChart): ApexOptions {
  const chart = modelChart as ChartTypes.RocCurveChart
  return {
    chart: { type: 'line' },
    title: { text: chart.title },
    xaxis: {
      title: { text: chart.x_axis },
      labels: {
        // value is the raw data point
        formatter: (value) => {
          if (typeof value === 'number') return value.toFixed(2)
          return value // Return as-is if it's a category string
        },
      },
    },
    yaxis: {
      title: { text: chart.y_axis },
      labels: {
        // value is the raw data point
        formatter: (value) => {
          if (typeof value === 'number') return value.toFixed(2)
          return value // Return as-is if it's a category string
        },
      },
    },
    labels: chart.legend || [],
  }
}

// Calibration Curve → Line
export function mapCalibrationCurve(modelChart: ChartTypes.ModelChart): ApexOptions {
  const chart = modelChart as ChartTypes.CalibrationCurveChart
  return {
    chart: { type: 'line' },
    title: { text: chart.title },
    xaxis: {
      title: { text: chart.x_axis },
      labels: {
        // value is the raw data point
        formatter: (value) => {
          if (typeof value === 'number') return value.toFixed(2)
          return value // Return as-is if it's a category string
        },
      },
    },
    yaxis: {
      title: { text: chart.y_axis },
      labels: {
        // value is the raw data point
        formatter: (value) => {
          if (typeof value === 'number') return value.toFixed(2)
          return value // Return as-is if it's a category string
        },
      },
    },
    labels: chart.legend || [],
  }
}

// Dynamic Renderer
export function mapChart(chart: ChartTypes.ModelChart): ApexOptions {
  // Switched from chart.type to chart.chart_type
  switch (chart.chart_type) {
    case 'feature_importance':
      return mapFeatureImportance(chart)

    case 'prediction_distribution':
      return mapPredictionDistribution(chart)

    case 'roc_curve':
      return mapRocCurve(chart)

    case 'confusion_matrix':
      return mapConfusionMatrix(chart)

    case 'calibration_curve':
      return mapCalibrationCurve(chart)

    default:
      // Exhaustive check for TypeScript
      const _exhaustiveCheck: never = chart
      throw new Error(`Unknown chart type: ${chart}`)
  }
}
