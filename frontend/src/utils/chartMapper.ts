import * as ModelChartTypes from '@/types/modelCharts'
import * as DataChartTypes from '@/types/datasetCharts'
import type { ApexOptions } from 'apexcharts'
import {
  mapFeatureImportance,
  mapCalibrationCurve,
  mapConfusionMatrix,
  mapPredictionDistribution,
  mapRocCurve,
} from './modelChartMappers'

import {
  mapCorrelationMatrix,
  mapMissingValues,
  mapBoxPlot,
  mapFeatureBarChart,
  mapXYChart,
  mapTargetDistribution,
} from './dataChartMappers'
import type { BaseChart } from '@/types/charts'

// Dynamic Renderer
export function mapChart(chart: BaseChart): ApexOptions {
  switch (chart.chart_type) {
    // model charts
    case 'feature_importance':
      return mapFeatureImportance(chart as ModelChartTypes.FeatureImportanceChart)

    case 'prediction_distribution':
      return mapPredictionDistribution(chart as ModelChartTypes.PredictionDistributionChart)

    case 'roc_curve':
      return mapRocCurve(chart as ModelChartTypes.RocCurveChart)

    case 'confusion_matrix':
      return mapConfusionMatrix(chart as ModelChartTypes.ConfusionMatrixChart)

    case 'calibration_curve':
      return mapCalibrationCurve(chart as ModelChartTypes.CalibrationCurveChart)
    // data charts
    case 'correlation_matrix':
      return mapCorrelationMatrix(chart as DataChartTypes.CorrelationMatrixChart)

    case 'target_distribution':
      return mapTargetDistribution(chart as DataChartTypes.TargetDistributionChart)

    case 'missing_values':
      return mapMissingValues(chart as DataChartTypes.MissingValuesChart)

    case 'boxplot':
      return mapBoxPlot(chart as DataChartTypes.BoxPlotChart)

    case 'xy':
      return mapXYChart(chart as DataChartTypes.XYChart)

    case 'categorical':
      return mapFeatureBarChart(chart as DataChartTypes.FeatureBarChart)

    default:
      // Exhaustive check for TypeScript
      throw new Error(`Unknown chart type: ${chart}`)
  }
}
