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
  mapFeatureDistribution,
  mapFeatureTargetRelationship,
  mapTargetDistribution,
  mapOutliers,
} from './dataChartMappers'

export type CommonChart = ModelChartTypes.ModelChart | DataChartTypes.DataChart

// Dynamic Renderer
export function mapChart(chart: CommonChart): ApexOptions {
  switch (chart.chart_type) {
    // model charts
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
    // data charts
    case 'correlation_matrix':
      return mapCorrelationMatrix(chart)

    case 'missing_values':
      return mapMissingValues(chart)

    case 'feature_distribution':
      return mapFeatureDistribution(chart)

    case 'feature_target_relationship':
      return mapFeatureTargetRelationship(chart)

    case 'outliers':
      return mapOutliers(chart)

    case 'target_distribution':
      return mapTargetDistribution(chart)

    default:
      // Exhaustive check for TypeScript
      const _exhaustiveCheck: never = chart
      throw new Error(`Unknown chart type: ${chart}`)
  }
}
