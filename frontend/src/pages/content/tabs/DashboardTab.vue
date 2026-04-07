<script setup lang="ts">
import DataTable from '@/components/shared/DataTable.vue'
import KpiCard from '@/components/shared/KpiCard.vue'
import BaseBadge from '@/components/ui/BaseBadge.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import { useDashboard } from '@/composables/useDashboard'
import { toDisplayPercentage } from '@/utils/formatter'
import { getStatusVariant } from '@/utils/tabular'
import { format } from 'date-fns'

const { error, kpiItems, stats, fetchMetrics } = useDashboard()

const headers = [
  { key: 'model', label: 'Model' },
  { key: 'dataset', label: 'Dataset' },
  { key: 'trained_at', label: 'Trained at' },
  { key: 'status', label: 'Status' },
  { key: 'accuracy', label: 'Accuracy' },
]
</script>

<template>
  <div class="dashboard-container">
    <div v-if="error" class="error-container">
      {{ error.message }}
      <BaseButton @click="fetchMetrics" :small="true" variant="danger">Retry</BaseButton>
    </div>
    <div class="stats-grid" role="region" aria-label="Key performance indicators">
      <KpiCard
        v-for="item in kpiItems"
        :key="item.key"
        :label="item.label"
        :icon="item.icon"
        :value="item.displayValue"
      />
    </div>
    <hr />

    <div class="middle-grid">
      <div class="card recent-activity">
        <h2>Recent Activity</h2>
        <hr />
        <p v-if="stats.recent_activity.length === 0">🔴 No recent activity</p>
        <p v-for="act in stats.recent_activity" :key="act">🔵 {{ act }}</p>
      </div>

      <div class="card quick-actions">
        <h2>Quick Actions</h2>
        <hr />
        <div class="quick-actions-btns">
          <router-link to="/app/upload" custom v-slot="{ navigate }">
            <BaseButton @click="navigate" role="link" :stretch="false"> Upload Dataset </BaseButton>
          </router-link>
          <router-link to="/app/datasets" custom v-slot="{ navigate }">
            <BaseButton @click="navigate" role="link" variant="secondary" :stretch="false"
              >Train Model</BaseButton
            >
          </router-link>
          <router-link to="/app/models" custom v-slot="{ navigate }">
            <BaseButton @click="navigate" role="link" variant="secondary" :stretch="false"
              >View Models</BaseButton
            >
          </router-link>
        </div>
      </div>
    </div>
    <hr />

    <div class="card table-card">
      <h3>Recent Models</h3>
      <DataTable :headers="headers" :items="stats.recent_models">
        <template #cell(model)="{ item }">
          <a href="#">{{ item.name }}</a>
        </template>
        <template #cell(dataset)="{ item }">
          <a href="#">{{ item.dataset_name }}</a>
        </template>
        <template #cell(status)="{ item }">
          <BaseBadge :variant="getStatusVariant(item.status)">
            {{ item.status }}
          </BaseBadge>
        </template>
        <template #cell(trained_at)="{ item }">
          {{ format(item.trained_at, 'MM/dd/yyyy hh:mm:ss') }}
        </template>
        <template #cell(accuracy)="{ item }">
          {{ toDisplayPercentage(item.accuracy) }}
        </template>
      </DataTable>
      <!--
        <table>
          <thead>
            <tr>
              <th>Model</th>
              <th>Dataset</th>
              <th>Trained at</th>
              <th>Status</th>
              <th>Accuracy</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="model in stats.recent_models" :key="model.id">
              <td class="row-id">{{ model.name }}</td>
              <td>{{ model.dataset_name }}</td>
              <td>{{ format(model.trained_at, 'MM/dd/yyyy hh:mm:ss') }}</td>
              <td :class="model.status">{{ model.status }}</td>
              <td>{{ toDisplayPercentage(model.accuracy) }}</td>
            </tr>
          </tbody>
        </table>
      -->
    </div>
  </div>
</template>

<style scoped>
.error-container {
  color: var(--error-text);
  margin: 1rem;
}
.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin: 1.5rem 0;
}
.middle-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-auto-rows: 1fr;
  gap: 20px;
  margin: 1rem 0;
}
.recent-activity {
}
.quick-actions {
}
.quick-actions-btns {
  display: flex;
  overflow: auto;
  flex-wrap: wrap;
  justify-content: center;
  gap: 1rem;
  margin-top: 1rem;
}
.card {
  background: white;
  padding: 24px;
  border-radius: 8px;
  border: 1px solid var(--gray-300);
}
.table-card {
  margin: 1rem 0;
}
.trained {
  font-weight: 500;
  color: var(--color-success);
}
.training {
  font-weight: 500;
  color: var(--gray-500);
}
.failed {
  font-weight: 500;
  color: var(--color-danger);
}
table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 16px;
}

th {
  text-align: left;
  background-color: var(--gray-100);
  font-weight: 500;
  padding: 1rem;
}
thead {
  border: 1px solid var(--gray-300);
}
tr {
  border: 1px solid var(--gray-300);
  background-color: var(--color-white);
}
td {
  padding: 16px 8px;
  border-bottom: 1px solid var(--gray-300);
}

h2 {
  margin: 0;
}
hr {
  border: 0;
  height: 1px;
  background-color: var(--gray-300);
}
</style>
