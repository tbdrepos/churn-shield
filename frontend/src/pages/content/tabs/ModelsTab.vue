<script setup lang="ts">
import BaseButton from '@/components/ui/BaseButton.vue'
import { useModels } from '@/composables/useModels'
import { toDisplayPercentage } from '@/utils/formatter'
import { getStatusVariant } from '@/utils/tabular'
import { useConfirmDialog } from '@vueuse/core'
import { format } from 'date-fns'
import { useRouter } from 'vue-router'

const { isRevealed, reveal, confirm, cancel } = useConfirmDialog()
const { models, isLoading, error, deleteModel } = useModels()
const router = useRouter()

const handleDelete = async (id: string) => {
  const { isCanceled } = await reveal()
  if (!isCanceled) {
    deleteModel(id)
  }
}

const viewModel = async (id: string) => {
  router.push({ name: 'dataset-details', params: { id: id } })
}

const headers = [
  { key: 'name', label: 'Name' },
  { key: 'dataset', label: 'Dataset' },
  { key: 'trained_at', label: 'Trained At' },
  { key: 'status', label: 'Status' },
  { key: 'accuracy', label: 'Accuracy' },
  { key: 'actions', label: 'Actions' },
]
</script>

<template>
  <header>
    <h1>Datasets</h1>
    <RouterLink to="/app/datasets" v-slot="{ navigate }">
      <BaseButton @click="navigate">
        <BaseIcon name="Brain" />
        Train models
      </BaseButton>
    </RouterLink>
  </header>
  <p v-if="isLoading">Loading...</p>
  <p v-else-if="error">Error: {{ error.message }}</p>
  <DataTable v-if="models" :headers="headers" :items="models">
    <template #cell(name)="{ item }">
      <a href="#">{{ item.name }}</a>
    </template>

    <template #cell(dataset)="{ item }">
      {{ item.dataset_name }}
    </template>

    <template #cell(trained_at)="{ item }">
      {{ format(item.trained_at, 'MM/dd/yyyy hh:mm:ss') }}
    </template>

    <template #cell(status)="{ item }">
      <BaseBadge :variant="getStatusVariant(item.status)">
        {{ item.status }}
      </BaseBadge>
    </template>

    <template #cell(accuracy)="{ item }">
      {{ toDisplayPercentage(item.accuracy) }}
    </template>

    <template #cell(actions)="{ item }">
      <BaseButton @click="viewModel(item.id)" variant="secondary" :small="true">View</BaseButton>
      <BaseButton @click="handleDelete(item.id)" variant="danger" :small="true">Delete</BaseButton>
    </template>
  </DataTable>

  <BaseConfirmDialog
    variant="danger"
    :reveal="isRevealed"
    title="Delete Model?"
    message="Are you sure you want to permanently delete this model?"
    confirm-text="Delete"
    @confirm="confirm"
    @cancel="cancel"
  />
</template>

<style scoped>
header {
  margin-bottom: 2rem;
}
</style>
