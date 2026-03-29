<script setup lang="ts">
import { useModels } from '@/composables/useModels'
import { useConfirmDialog } from '@vueuse/core'

const { isRevealed, reveal, confirm, cancel } = useConfirmDialog()
const { models, loading, error, viewModel, deleteModel } = useModels()

const handleDelete = async (id: string) => {
  const { isCanceled } = await reveal()
  if (!isCanceled) {
    deleteModel(id)
  }
}
</script>

<template>
  <p v-if="loading">Loading...</p>
  <p v-else-if="error">Error: {{ error.message }}</p>
  <table border="1" cellpadding="8" v-if="models">
    <thead>
      <tr>
        <th>ID</th>
        <th>Dataset</th>
        <th>Trained at</th>
        <th>Actions</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="model in models" :key="model.id">
        <td>{{ model.id }}</td>
        <td>{{ model.dataset_id }}</td>
        <td>{{ model.trained_at }}</td>
        <td>
          <button @click="viewModel(model.id)">View</button>
          <button @click="handleDelete(model.id)">Delete</button>
        </td>
      </tr>
    </tbody>
  </table>
  <p v-else-if="!loading">No models found.</p>
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

  box-shadow: 0 4px 6px rgba(190, 186, 186, 0.1);
}
.btn-danger {
  background: #ff4d4d;
  color: white;
}
</style>
