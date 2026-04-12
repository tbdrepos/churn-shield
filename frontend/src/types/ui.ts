export interface SelectOption {
  label: string
  value: string | number
}

export interface Tab {
  label: string
  value: string
}

export interface InsightTabs {
  model: Tab
  data: Tab
}
