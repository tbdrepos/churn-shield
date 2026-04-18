import * as ChartTypes from '@/types/datasetCharts'
import type { ApexOptions } from 'apexcharts'

// =========================================================
// HELPERS FOR CATEGORICAL DATA
// =========================================================

export function mapMissingValues(chart: ChartTypes.MissingValuesChart): ApexOptions {
  return {
    chart: { type: 'bar' },
    title: { text: chart.title },
    subtitle: { text: chart.description },
    xaxis: {
      type: 'category',
      categories: chart.categories,
      title: { text: chart.x_axis || 'Features' },
    },
    yaxis: {
      title: { text: chart.y_axis || 'Missing Count' },
    },
    series: [
      {
        name: 'Missing Count',
        data: chart.series,
      },
    ],
    tooltip: {
      y: {
        formatter: (val, { dataPointIndex }) => {
          const pct = (chart.percentages[dataPointIndex] * 100).toFixed(2)
          return `${val} (${pct}%)`
        },
      },
    },
  }
}

export function mapTargetDistribution(chart: ChartTypes.TargetDistributionChart): ApexOptions {
  return {
    chart: { type: 'bar' },
    title: { text: chart.title },
    subtitle: { text: chart.description },
    xaxis: {
      type: 'category',
      categories: chart.categories,
    },
    series: [
      {
        name: 'Count',
        data: chart.series,
      },
    ],
  }
}

// =========================================================
// CORRELATION MATRIX (HEATMAP)
// =========================================================

export function mapCorrelationMatrix(chart: ChartTypes.CorrelationMatrixChart): ApexOptions {
  return {
    chart: { type: 'heatmap' },
    title: { text: chart.title },
    subtitle: { text: chart.description },
    xaxis: {
      type: 'category',
      // The categories are the labels provided by the backend
      categories: chart.labels,
    },
    // Backend CorrelationSeries matches Apex [{ name: string, data: {x, y}[] }]
    series: chart.series,
    plotOptions: {
      heatmap: {
        colorScale: {
          ranges: [
            { from: -1, to: -0.5, color: '#D32F2F', name: 'Strong Negative' },
            { from: -0.5, to: 0.5, color: '#9c713d', name: 'Weak/Neutral' },
            { from: 0.5, to: 1, color: '#388E3C', name: 'Strong Positive' },
          ],
        },
      },
    },
  }
}

// =========================================================
// COMPOSITE MAPPERS (SUB-CHART RENDERING)
// =========================================================

/**
 * Maps an individual BoxPlot from the Outliers composite
 */
export function mapBoxPlot(chart: ChartTypes.BoxPlotChart): ApexOptions {
  return {
    chart: { type: 'boxPlot' },
    title: { text: chart.title },
    xaxis: { type: 'category' },
    series: [
      {
        type: 'boxPlot',
        data: [
          {
            x: chart.title,
            y: chart.series, // [lower, q1, median, q3, upper]
          },
        ],
      },
    ],
  }
}

/**
 * Maps an individual XY plot from Relationship composite
 */
export function mapXYChart(chart: ChartTypes.XYChart): ApexOptions {
  return {
    chart: { type: 'line' }, // or 'scatter' depending on preference
    title: { text: chart.title },
    xaxis: { title: { text: chart.x_axis } },
    yaxis: { title: { text: chart.y_axis } },
    series: chart.series.map((dataArray, index) => ({
      name: chart.legend?.[index] || 'Series',
      data: dataArray,
    })),
  }
}

/**
 * Maps an individual BarChart from the FeatureDistribution composite
 */
export function mapFeatureBarChart(chart: ChartTypes.FeatureBarChart): ApexOptions {
  return {
    chart: { type: 'bar' },
    title: { text: chart.title },
    xaxis: {
      categories: chart.categories,
      title: { text: chart.x_axis },
    },
    series: [
      {
        name: chart.title,
        data: chart.series,
      },
    ],
  }
}
