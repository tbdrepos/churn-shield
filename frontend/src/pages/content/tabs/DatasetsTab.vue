<script setup lang="ts">
import { useDatasets } from '@/composables/useDatasets'
import { useConfirmDialog } from '@vueuse/core'
import { useRouter } from 'vue-router'

const { isRevealed, reveal, confirm, cancel } = useConfirmDialog()
const { datasets, loading, error, trainDataset, deleteDataset } = useDatasets()
const router = useRouter()

const handleDelete = async (id: string) => {
  const { isCanceled } = await reveal()
  if (!isCanceled) {
    deleteDataset(id)
  }
}

const viewDataset = async (id: string) => {
  router.push({ name: 'dataset-details', params: { id: id } })
}
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
          <button @click="viewDataset(dataset.id)">View</button>

          <button v-if="dataset.status !== 'training'" @click="trainDataset(dataset.id)">
            {{ dataset.status === 'trained' ? 'Retrain' : 'Train' }}
          </button>

          <button @click="handleDelete(dataset.id)">Delete</button>
        </td>
      </tr>
    </tbody>
  </table>
  <teleport to="body">
    <div v-if="isRevealed" class="modal-overlay">
      <div class="modal-content">
        <h3>Delete Dataset?</h3>
        <p>This action cannot be undone.</p>
        <div class="modal-actions">
          <button @click="cancel">Cancel</button>
          <button @click="confirm" class="btn-danger">Confirm Delete</button>
        </div>
      </div>
    </div>
  </teleport>
</template>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-content {
  background: var(--surface-color);

  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.btn-danger {
  background: #ff4d4d;
  color: white;
}
</style>
