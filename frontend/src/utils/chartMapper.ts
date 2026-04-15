import * as ChartTypes from '@/types/apiCharts'
import * as ApexTypes from '@/types/apexCharts'

// Feature Importance → Bar Chart
export function mapFeatureImportance(
  chart: ChartTypes.FeatureImportanceChart,
): ApexTypes.BarChartOptions {
  return {
    series: [
      {
        name: 'Importance',
        data: chart.series,
      },
    ],
    categories: chart.categories,
  }
}

// Prediction Distribution → Donut
export function mapPredictionDistribution(
  chart: ChartTypes.PredictionDistributionChart,
): ApexTypes.DonutChartOptions {
  return {
    series: chart.series,
    labels: chart.categories,
  }
}

// ROC Curve → Line
export function mapRocCurve(chart: ChartTypes.RocCurveChart): ApexTypes.LineChartOptions {
  return {
    // The backend already formatted this as [{ x, y }] inside the series
    series: chart.series.map((s) => ({
      name: `${s.name} (AUC: ${chart.auc.toFixed(2)})`,
      data: s.data,
    })),
  }
}

// Confusion Matrix → Heatmap
export function mapConfusionMatrix(
  chart: ChartTypes.ConfusionMatrixChart,
): ApexTypes.HeatmapChartOptions {
  return {
    // Backend series represents rows, each data point has { x: pred_label, y: probability }
    series: chart.series.map((row) => ({
      name: row.name, // Actual Label
      data: row.data.map((cell) => ({
        x: cell.x, // Predicted Label
        y: cell.y, // Normalized Value
        // Note: ApexCharts allows extra properties in data for custom tooltips
        count: cell.count,
      })),
    })),
  }
}

// Calibration Curve → Line
export function mapCalibrationCurve(
  chart: ChartTypes.CalibrationCurveChart,
): ApexTypes.LineChartOptions {
  return {
    series: chart.series.map((s) => ({
      name: s.name,
      // Backend provides [pred, true], map to { x, y } for Apex
      data: s.data.map(([pred, trueVal]) => ({
        x: pred,
        y: trueVal,
      })),
    })),
  }
}

// Dynamic Renderer
export function mapChart(chart: ChartTypes.ModelChart): ApexTypes.ApexChartOption {
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
