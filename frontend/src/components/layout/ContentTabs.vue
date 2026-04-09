<script setup lang="ts">
import { ref } from 'vue'
import BaseTabs from '@/components/ui/BaseTabs.vue'
import ModelDetails from '@/pages/content/tabs/ModelDetails.vue'
import DatasetDetails from '@/pages/content/tabs/DatasetDetails.vue'

const currentTab = ref('model')

const tabs = [
  { label: 'Model Insights', value: 'model' },
  { label: 'Data Insights', value: 'data' },
]
</script>
<template>
  <div class="dashboard-page">
    <BaseTabs v-model="currentTab" :tabs="tabs">
      <template #model>
        <ModelDetails />
      </template>
      <template #data>
        <DatasetDetails />
      </template>
    </BaseTabs>
  </div>
</template>

<style lang="css" scoped>
.dashboard-page {
}
</style>
