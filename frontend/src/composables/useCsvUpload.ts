// @/composables/useCsvUpload.ts
import { ref } from 'vue'
import Papa from 'papaparse'
import { ApiError, apiFetch } from '@/utils/api'

export function useCsvUpload(endpoint: string) {
  const file = ref<File | null>(null)
  const preview = ref<string[][]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  /**
   * Internal helper to parse the file using PapaParse
   */
  const parseFile = (selectedFile: File): Promise<string[][]> => {
    return new Promise((resolve, reject) => {
      Papa.parse(selectedFile, {
        header: false, // We want raw arrays to handle the preview ourselves
        preview: 6, // Only parse the first 6 rows for efficiency
        skipEmptyLines: 'greedy',
        complete: (results) => resolve(results.data as string[][]),
        error: (err) => reject(err),
      })
    })
  }

  const handleFileChange = async (files: FileList | File[] | null) => {
    if (!files?.length) return

    const selectedFile = files[0]

    if (!selectedFile) {
      error.value = 'Could not read file.'
      return false
    }

    const isCsvMime = selectedFile.type === 'text/csv'
    const isCsvExt = selectedFile.name.toLowerCase().endsWith('.csv')
    if (!isCsvMime && !isCsvExt) {
      error.value = 'Please upload a valid CSV file.'
      return false
    }

    error.value = null
    file.value = selectedFile

    try {
      preview.value = await parseFile(selectedFile)
    } catch (e) {
      error.value = 'Failed to parse CSV. The file might be corrupted.'
      console.error('PapaParse Error:', e)
    }
  }

  const upload = async (): Promise<boolean> => {
    if (!file.value) return false

    loading.value = true
    error.value = null

    const formData = new FormData()
    formData.append('file', file.value)

    try {
      await apiFetch(endpoint, {
        method: 'POST',
        body: formData,
        credentials: 'include',
      })
      reset()
      return true
    } catch (err) {
      error.value = err instanceof ApiError ? err.message : 'Upload failed.'
      return false
    } finally {
      loading.value = false
    }
  }

  const reset = () => {
    file.value = null
    preview.value = []
    error.value = null
  }

  return {
    file,
    preview,
    loading,
    error,
    handleFileChange,
    upload,
    reset,
  }
}
