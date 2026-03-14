<script setup lang="ts">
import { ref } from 'vue'
import { useDropZone, useFileDialog } from '@vueuse/core'
import { ApiError, apiFetch } from '@/utils/api'

const dropZoneRef = ref<HTMLElement | null>(null)

const file = ref<File | null>(null)
const preview = ref<string[][]>([])
const loading = ref(false)
const error = ref<string | null>(null)

/* ---------------------------
   File Picker
---------------------------- */

const { open, onChange } = useFileDialog({
  accept: '.csv',
})

onChange(async (files) => {
  if (!files?.length) return

  file.value = files[0] as File
  await generatePreview(file.value)
})

/* ---------------------------
   Drag and Drop
---------------------------- */

useDropZone(dropZoneRef, {
  onDrop: async (files) => {
    if (!files?.length) return

    file.value = files[0] as File
    await generatePreview(file.value)
  },
})

/* ---------------------------
   CSV Preview
---------------------------- */

async function generatePreview(file: File) {
  const text = await file.text()

  const rows = text.split('\n').slice(0, 6)

  preview.value = rows.map((row) => row.split(','))
}

/* ---------------------------
   Upload Dataset
---------------------------- */

async function upload() {
  if (!file.value) return

  loading.value = true
  error.value = null

  const form = new FormData()
  form.append('file', file.value)

  try {
    const res = await apiFetch('/upload', {
      method: 'POST',
      body: form,
      credentials: 'include',
    })
    alert('Dataset uploaded successfully')

    file.value = null
    preview.value = []
  } catch (err) {
    if (err instanceof ApiError) {
      console.error(`API error ${err.status}: ${err.message}\n${err.error}`)
    } else {
      console.error('Unexpected error:', err)
    }
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="page">
    <h1>Upload Dataset</h1>

    <!-- Drop Zone -->
    <div ref="dropZoneRef" class="dropzone">
      <p v-if="!file">Drag & drop your CSV file here</p>

      <p v-else>Selected: {{ file.name }}</p>

      <button @click="open">Select File</button>
    </div>

    <!-- Upload Button -->
    <button class="upload-btn" :disabled="!file || loading" @click="upload">
      {{ loading ? 'Uploading...' : 'Upload Dataset' }}
    </button>

    <!-- Error -->
    <p v-if="error" class="error">
      {{ error }}
    </p>

    <!-- Preview -->
    <div v-if="preview.length" class="preview">
      <h2>Preview</h2>

      <table>
        <tbody>
          <tr v-for="(row, i) in preview" :key="i">
            <td v-for="(col, j) in row" :key="j">
              {{ col }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<style scoped>
.page {
  max-width: 900px;
  margin: auto;
}

h1 {
  margin-bottom: 20px;
}

/* Dropzone */

.dropzone {
  border: 2px dashed #f5c0c0;
  border-radius: 12px;
  padding: 40px;
  text-align: center;
  background: #1e1d2b;
  margin-bottom: 20px;
}

.dropzone button {
  margin-top: 15px;
}

/* Upload Button */

.upload-btn {
  background: #f5c0c0;
  color: #15141d;
  border: none;
  padding: 10px 20px;
  border-radius: 8px;
  cursor: pointer;
}

.upload-btn:disabled {
  opacity: 0.6;
}

/* Error */

.error {
  color: #ff6b6b;
  margin-top: 10px;
}

/* Preview */

.preview {
  margin-top: 30px;
}

table {
  width: 100%;
  border-collapse: collapse;
}

td {
  border-bottom: 1px solid #333;
  padding: 6px;
}
</style>
