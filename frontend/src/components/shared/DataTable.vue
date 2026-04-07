<script setup lang="ts" generic="T">
defineProps<{
  headers: { key: string; label: string; width?: string }[]
  items: T[]
  loading?: boolean
}>()
</script>

<template>
  <div class="table-container">
    <table class="base-table">
      <thead>
        <tr>
          <th v-for="header in headers" :key="header.key" :style="{ width: header.width }">
            {{ header.label }}
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-if="loading">
          <td :colspan="headers.length" class="text-center">Loading...</td>
        </tr>
        <tr v-else-if="items.length === 0">
          <td :colspan="headers.length" class="text-center">No data found.</td>
        </tr>
        <tr v-for="(item, index) in items" :key="index">
          <td v-for="header in headers" :key="header.key">
            <slot :name="`cell(${header.key})`" :item="item">
              {{ (item as any)[header.key] }}
            </slot>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style scoped>
.table-container {
  background: white;
  border: 1px solid #e0e4e8;
  border-radius: 8px;
  overflow: hidden;
}

.base-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
}

thead {
  background-color: #f8fafb;
  border-bottom: 1px solid #e0e4e8;
}

th {
  padding: 1rem;
  color: var(--gray--300);
  font-size: 0.875rem;
  font-weight: 600;
}

td {
  padding: 1rem;
  border-bottom: 1px solid var(--gray--100);
  color: var(--gray--700);
  font-size: 0.9rem;
  vertical-align: middle;
}

tr:last-child td {
  border-bottom: none;
}

:deep(a),
.link {
  color: var(--color-primary);
  text-decoration: none;
  font-weight: 500;
}

:deep(a:hover) {
  text-decoration: underline;
}

.text-center {
  text-align: center;
  padding: 2rem;
}
</style>
