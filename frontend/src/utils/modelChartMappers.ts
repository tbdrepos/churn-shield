import * as ChartTypes from '@/types/modelCharts'
import type { ApexOptions } from 'apexcharts'

// Feature Importance → Bar Chart
export function mapFeatureImportance(modelChart: ChartTypes.ModelChart): ApexOptions {
  const chart = modelChart as ChartTypes.FeatureImportanceChart
  return {
    chart: { type: 'bar' },
    title: { text: chart.title },
    subtitle: { text: chart.description },
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
    series: chart.series,
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

    subtitle: { text: chart.description },
    labels: chart.categories || [],
    series: chart.series,
  }
}

// Confusion Matrix → Heatmap
export function mapConfusionMatrix(modelChart: ChartTypes.ModelChart): ApexOptions {
  const chart = modelChart as ChartTypes.ConfusionMatrixChart
  return {
    chart: { type: 'heatmap' },
    title: { text: chart.title },

    subtitle: { text: chart.description },
    labels: chart.labels || [],
    series: chart.series,
  }
}

// ROC Curve → Line
export function mapRocCurve(modelChart: ChartTypes.ModelChart): ApexOptions {
  const chart = modelChart as ChartTypes.RocCurveChart
  return {
    chart: { type: 'line' },
    title: { text: chart.title },
    stroke: {
      curve: 'stepline',
      width: 3,
    },
    subtitle: { text: chart.description },
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
    series: chart.series,
  }
}

// Calibration Curve → Line
export function mapCalibrationCurve(modelChart: ChartTypes.ModelChart): ApexOptions {
  const chart = modelChart as ChartTypes.CalibrationCurveChart
  return {
    chart: { type: 'line' },
    title: { text: chart.title },
    subtitle: { text: chart.description },
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
    series: chart.series,
  }
}
