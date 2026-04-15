export interface BarChartSeries {
  name: string
  data: number[]
}

export interface BarChartOptions {
  series: BarChartSeries[]
  categories: string[]
}

export interface DonutChartOptions {
  series: number[]
  labels: string[]
}

export interface LineChartSeries {
  name: string
  data: { x: number; y: number }[]
}

export interface LineChartOptions {
  series: LineChartSeries[]
}

export interface HeatmapChartOptions {
  series: {
    name: string
    data: { x: string; y: number }[]
  }[]
}

export type ApexChartOption =
  | BarChartOptions
  | DonutChartOptions
  | LineChartOptions
  | HeatmapChartOptions
