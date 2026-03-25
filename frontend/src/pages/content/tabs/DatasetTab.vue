<script setup lang="ts">
import { useDatasets } from '@/composables/useDatasets'

const { datasets, loading, error, trainDataset, deleteDataset } = useDatasets()
</script>

<template>
  <header>
    <h1>Datasets</h1>
    <RouterLink to="/app/upload" v-slot="{ navigate }">
      <button @click="navigate">+Upload Dataset</button>
    </RouterLink>
  </header>
  <hr />
  <p v-if="loading">Loading...</p>
  <p v-else-if="error">Error: {{ error.message }}</p>
  <table border="1" cellpadding="8" v-if="datasets">
    <thead>
      <tr>
        <th>Name</th>
        <th>Rows</th>
        <th>Uploaded</th>
        <th>Status</th>
        <th>Actions</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="dataset in datasets" :key="dataset.id">
        <td>{{ dataset.original_name }}</td>
        <td>{{ dataset.row_count }}</td>
        <td>{{ dataset.uploaded_at }}</td>
        <td>{{ dataset.status }}</td>
        <td>
          <button @click="$emit('view', dataset)">View</button>

          <button v-if="dataset.status !== 'training'" @click="trainDataset(dataset.id)">
            {{ dataset.status === 'trained' ? 'Retrain' : 'Train' }}
          </button>

          <button @click="deleteDataset(dataset.id)">Delete</button>
        </td>
      </tr>
    </tbody>
  </table>
</template>

<style scoped></style>
