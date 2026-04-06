<script setup lang="ts">
import { ref, computed } from 'vue'
import { useDropZone, useFileDialog } from '@vueuse/core'
import { useCsvUpload } from '@/composables/useCsvUpload'
import { schema } from '@/composables/useDatasets'

// UI Components
import BaseButton from '@/components/ui/BaseButton.vue'
import BaseAlert from '@/components/ui/BaseAlert.vue'
import BaseIcon from '@/components/ui/BaseIcon.vue'
import { useToastStore } from '@/stores/toastStore'

const dropZoneRef = ref<HTMLElement | null>(null)
const toast = useToastStore()

// 1. Initialize the Composable
const {
  file,
  preview,
  loading,
  error,
  handleFileChange,
  upload,
  reset
} = useCsvUpload('/datasets/upload')

// 2. Setup File Dialog (VueUse)
const { open, onChange } = useFileDialog({
  accept: '.csv',
  multiple: false
})
onChange(handleFileChange)

// 3. Setup Drag and Drop (VueUse)
const { isOverDropZone } = useDropZone(dropZoneRef, {
  onDrop: handleFileChange
})

// 4. Computed Table Data
const previewHeaders = computed(() => preview.value.length > 0 ? preview.value[0] : [])
const previewRows = computed(() => preview.value.length > 1 ? preview.value.slice(1) : [])

const onUploadClick = async () => {
  const success = await upload()
  if (success) {
    toast.addToast('Dataset uploaded successfully!', 'success')
  } else {
    toast.addToast('Upload failed. Please check your file.', 'error')
  }
}
</script>

<template>
  <div class="page-container">
    <header class="page-header">
      <div class="title-group">
        <BaseIcon name="Database" :size="32" color="var(--color-primary)" />
        <h1>Upload Dataset</h1>
      </div>
      <BaseButton v-if="file" variant="secondary" size="sm" @click="reset">
        Clear Selection
      </BaseButton>
    </header>

    <section ref="dropZoneRef" class="dropzone" :class="{ 'is-over': isOverDropZone, 'has-file': file }"
      @click="() => !file && open()">
      <div class="dropzone-inner">
        <BaseIcon :name="file ? 'FileCheck' : 'CloudUpload'" :size="48"
          :color="file ? 'var(--color-success)' : 'var(--gray-500)'" />

        <div v-if="!file" class="dropzone-text">
          <p class="main-text">Drag & drop your CSV file here</p>
          <p class="sub-text">or click to browse files</p>
        </div>

        <div v-else class="file-info">
          <p class="file-name">{{ file.name }}</p>
          <p class="file-size">{{ (file.size / 1024).toFixed(2) }} KB</p>
        </div>
      </div>
    </section>

    <div class="action-bar">
      <BaseButton size="lg" :loading="loading" :disabled="!file" class="upload-btn" @click="onUploadClick">
        <BaseIcon name="Send" :size="18" class="mr-2" />
        Process and Upload
      </BaseButton>
    </div>

    <BaseAlert v-if="error" :message="error" type="error" />

    <Transition name="fade" mode="out-in">
      <section v-if="preview.length" class="table-section" key="preview">
        <div class="section-title">
          <BaseIcon name="Table" :size="20" />
          <h2>Data Preview</h2>
        </div>
        <div class="table-wrapper">
          <table>
            <thead>
              <tr>
                <th v-for="(h, i) in previewHeaders" :key="i">{{ h }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(row, i) in previewRows" :key="i">
                <td v-for="(cell, j) in row" :key="j">{{ cell }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <section v-else class="table-section" key="schema">
        <div class="section-title">
          <BaseIcon name="Info" :size="20" />
          <h2>Expected CSV Structure</h2>
        </div>
        <div class="table-wrapper">
          <table class="schema-table">
            <thead>
              <tr>
                <th>Column</th>
                <th>Type</th>
                <th>Validation</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="col in schema" :key="col.name">
                <td><strong>{{ col.name }}</strong></td>
                <td><code>{{ col.type }}</code></td>
                <td class="sub-text">{{ col.values || 'Any value' }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>
    </Transition>
  </div>
</template>

<style scoped>
.page-container {
  max-width: 1000px;
  margin: 3rem auto;
  padding: 0 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.title-group {
  display: flex;
  align-items: center;
  gap: 1rem;
}

/* Dropzone Styles */
.dropzone {
  border: 2px dashed var(--gray-700);
  background: var(--surface-2-color);
  border-radius: 1rem;
  padding: 4rem 2rem;
  transition: all 0.25s ease;
  cursor: pointer;
}

.dropzone.is-over {
  border-color: var(--color-primary);
  background: color-mix(in srgb, var(--color-primary), transparent 95%);
  transform: translateY(-2px);
}

.dropzone.has-file {
  border-style: solid;
  border-color: var(--color-success);
}

.dropzone-inner {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.main-text {
  font-weight: 600;
  font-size: 1.1rem;
  margin: 0;
}

.sub-text {
  opacity: 0.6;
  font-size: 0.9rem;
  margin: 0;
}

.file-name {
  font-weight: 700;
  color: var(--color-success);
  margin: 0;
}

/* Table Styles */
.table-section {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 0.6rem;
}

.table-wrapper {
  overflow-x: auto;
  border: 1px solid var(--gray-800);
  border-radius: 0.75rem;
  background: var(--surface-1-color);
}

table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.875rem;
}

th {
  background: var(--gray-900);
  padding: 1rem;
  text-align: left;
  border-bottom: 2px solid var(--gray-800);
}

td {
  padding: 0.8rem 1rem;
  border-bottom: 1px solid var(--gray-800);
}

.upload-btn {
  width: 100%;
}

.mr-2 {
  margin-right: 0.5rem;
}

/* Transitions */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>