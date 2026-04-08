<script setup lang="ts">
import DataTable from '@/components/shared/DataTable.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import { useDatasets } from '@/composables/useDatasets'
import { useConfirmDialog } from '@vueuse/core'
import { useRouter } from 'vue-router'
import { format } from 'date-fns'
import BaseBadge from '@/components/ui/BaseBadge.vue'
import { getStatusVariant } from '@/utils/tabular'
import BaseConfirmDialog from '@/components/ui/BaseConfirmDialog.vue'
import BaseIcon from '@/components/ui/BaseIcon.vue'

const { isRevealed, reveal, confirm, cancel } = useConfirmDialog()
const { datasets, loading, error, trainDataset, deleteDataset, isDeleting, isTraining } =
  useDatasets()
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

const headers = [
  { key: 'name', label: 'Name' },
  { key: 'row_count', label: 'Row Count' },
  { key: 'uploaded_at', label: 'Uploaded At' },
  { key: 'status', label: 'Status' },
  { key: 'actions', label: 'Actions' },
]
</script>

<template>
  <header>
    <h1>Datasets</h1>
    <RouterLink to="/app/upload" v-slot="{ navigate }">
      <BaseButton @click="navigate">
        <BaseIcon name="CirclePlus" />
        Upload Dataset
      </BaseButton>
    </RouterLink>
  </header>
  <p v-if="loading">Loading...</p>
  <p v-else-if="error">Error: {{ error.message }}</p>
  <DataTable v-if="datasets" :headers="headers" :items="datasets">
    <template #cell(name)="{ item }">
      <a href="#">{{ item.original_name }}</a>
    </template>

    <template #cell(row_count)="{ item }">
      {{ item.row_count }}
    </template>

    <template #cell(uploaded_at)="{ item }">
      {{ format(item.uploaded_at, 'MM/dd/yyyy hh:mm:ss') }}
    </template>

    <template #cell(status)="{ item }">
      <BaseBadge :variant="getStatusVariant(item.status)">
        {{ item.status }}
      </BaseBadge>
    </template>

    <template #cell(actions)="{ item }">
      <BaseButton
        @click="trainDataset(item.id)"
        variant="primary"
        :small="true"
        :disabled="isDeleting || isTraining"
      >
        {{ item.status === 'trained' ? 'Retrain' : 'Train' }}
      </BaseButton>
      <BaseButton
        @click="viewDataset(item.id)"
        variant="secondary"
        :small="true"
        :disabled="isDeleting || isTraining"
        >View</BaseButton
      >
      <BaseButton
        @click="handleDelete(item.id)"
        variant="danger"
        :small="true"
        :disabled="isDeleting || isTraining"
        >Delete</BaseButton
      >
    </template>
  </DataTable>
  <BaseConfirmDialog
    variant="danger"
    :reveal="isRevealed"
    title="Delete Dataset?"
    message="Are you sure you want to delete this dataset? This will permanently remove all associated trained models."
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
