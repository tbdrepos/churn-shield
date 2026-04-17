import * as ChartTypes from '@/types/datasetCharts'
import type { ApexOptions } from 'apexcharts'

export function mapCorrelationMatrix(chart: ChartTypes.CorrelationMatrixChart): ApexOptions {
  return {
    chart: { type: 'heatmap' },
    title: { text: chart.title },
    subtitle: { text: chart.description },
    xaxis: {
      title: { text: chart.x_axis },
    },
    yaxis: {
      title: { text: chart.y_axis },
    },
    labels: chart.labels,
  }
}

export function mapMissingValues(chart: ChartTypes.MissingValuesChart): ApexOptions {
  return {
    chart: { type: 'bar' },
    title: { text: chart.title },
    subtitle: { text: chart.description },
    xaxis: {
      title: { text: chart.x_axis },
    },
    yaxis: {
      title: { text: chart.y_axis },
    },
  }
}

export function mapFeatureDistribution(chart: ChartTypes.FeatureDistributionChart): ApexOptions {
  return {
    chart: { type: 'bar' },
    title: { text: chart.title },
    subtitle: { text: chart.description },
    xaxis: {
      title: { text: chart.x_axis },
    },
    yaxis: {
      title: { text: chart.y_axis },
    },
  }
}

export function mapFeatureTargetRelationship(
  chart: ChartTypes.FeatureTargetRelationshipChart,
): ApexOptions {
  return {
    chart: { type: 'scatter' },
    title: { text: chart.title },
    subtitle: { text: chart.description },
    xaxis: {
      title: { text: chart.x_axis },
    },
    yaxis: {
      title: { text: chart.y_axis },
    },
  }
}

export function mapTargetDistribution(chart: ChartTypes.TargetDistributionChart): ApexOptions {
  return {
    chart: { type: 'bar' },
    title: { text: chart.title },
    subtitle: { text: chart.description },
    xaxis: {
      title: { text: chart.x_axis },
    },
    yaxis: {
      title: { text: chart.y_axis },
    },
  }
}

export function mapOutliers(chart: ChartTypes.OutliersChart): ApexOptions {
  return {
    chart: { type: 'boxPlot' },
    title: { text: chart.title },
    subtitle: { text: chart.description },
    xaxis: {
      title: { text: chart.x_axis },
    },
    yaxis: {
      title: { text: chart.y_axis },
    },
  }
}
