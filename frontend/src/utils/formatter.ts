export function toDisplayPercentage(raw: number | null | undefined): string {
  if (raw == null || Number.isNaN(raw)) return '0%'
  const formatter = new Intl.NumberFormat('en-US', {
    style: 'percent',
    minimumFractionDigits: 2, // Controls decimals: 75.60%
    maximumFractionDigits: 2,
  })
  return formatter.format(raw)
}
