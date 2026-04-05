<script setup lang="ts">
import KpiCard from '@/components/shared/KpiCard.vue'
import { useDashboard } from '@/composables/useDashboard'

const { error, kpiItems, stats, fetchMetrics } = useDashboard()
</script>

<template>
  <div class="dashboard-container">
    <div v-if="error && false" class="error-container">
      {{ error.message }}
      <button @click="fetchMetrics">Retry</button>
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
        <p v-for="act in stats.recent_activity" :key="act">{{ act }}</p>
      </div>

      <div class="card quick-actions">
        <router-link to="/app/upload" custom v-slot="{ navigate }">
          <button @click="navigate" role="link" class="btn primary">Upload Dataset</button>
        </router-link>
        <router-link to="/app/datasets" custom v-slot="{ navigate }">
          <button @click="navigate" role="link" class="btn">Train Model</button>
        </router-link>
        <router-link to="/app/models" custom v-slot="{ navigate }">
          <button @click="navigate" role="link" class="btn">View Models</button>
        </router-link>
      </div>
    </div>
    <hr />

    <div class="card table-card">
      <h3>Recent Models</h3>
      <table border="1" cellpadding="8">
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
            <td>{{ model.name }}</td>
            <td>{{ model.dataset_name }}</td>
            <td>{{ model.trained_at }}</td>
            <td>{{ model.status }}</td>
            <td>{{ model.accuracy }}</td>
          </tr>
        </tbody>
      </table>
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
  margin: 1rem 0;
}
.middle-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin: 1rem 0;
}

.card {
  background: white;
  padding: 24px;
  border-radius: 8px;
  border: 1px solid var(--border-color);
}
</style>
