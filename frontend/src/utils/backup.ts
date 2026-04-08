// const dropZoneRef = ref<HTMLElement | null>(null)

// const file = ref<File | null>(null)
// const preview = ref<string[][]>([])
// const loading = ref(false)
// const error = ref<string | null>(null)

// /* ---------------------------
//    File Picker
// ---------------------------- */

// const { open, onChange } = useFileDialog({
//   accept: '.csv',
// })

// onChange(async (files) => {
//   if (!files?.length) return

//   file.value = files[0] as File
//   await generatePreview(file.value)
// })

// /* ---------------------------
//    Drag and Drop
// ---------------------------- */

// useDropZone(dropZoneRef, {
//   onDrop: async (files) => {
//     if (!files?.length) return

//     file.value = files[0] as File
//     await generatePreview(file.value)
//   },
// })

// /* ---------------------------
//    CSV Preview
// ---------------------------- */

// async function generatePreview(file: File) {
//   const text = await file.text()
//   // take the first 6 rows as 1D array
//   const rows = text.split('\n').slice(0, 6)
//   // split each row into values to create a 2D array
//   preview.value = rows.map((row) => row.split(','))
// }

// /* ---------------------------
//    Upload Dataset
// ---------------------------- */

// async function upload() {
//   if (!file.value) return

//   loading.value = true
//   error.value = null

//   const form = new FormData()
//   form.append('file', file.value)

//   try {
//     const res = await apiFetch('/datasets/upload', {
//       method: 'POST',
//       body: form,
//       credentials: 'include',
//     })
//     alert('Dataset uploaded successfully')

//     file.value = null
//     preview.value = []
//   } catch (err) {
//     let errorMsg = ''
//     if (err instanceof ApiError) {
//       errorMsg = `API error ${err.status}: ${err.message}\n${err.error}`
//     } else {
//       errorMsg = `Unexpected error: ${err}`
//     }
//     console.error(errorMsg)
//     error.value = errorMsg
//   } finally {
//     loading.value = false
//   }
// }
/*
<!--
        <table>
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
              <td class="row-id">{{ model.name }}</td>
              <td>{{ model.dataset_name }}</td>
              <td>{{ format(model.trained_at, 'MM/dd/yyyy hh:mm:ss') }}</td>
              <td :class="model.status">{{ model.status }}</td>
              <td>{{ toDisplayPercentage(model.accuracy) }}</td>
            </tr>
          </tbody>
        </table>
      -->

*/
