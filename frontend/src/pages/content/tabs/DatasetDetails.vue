<script setup lang="ts">
import { watchEffect, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

// Computed property keeps the ID reactive if the URL changes
const datasetId = computed(() => {
  const id = route.params.id
  return Array.isArray(id) ? id[0] : id
})

// watcher in case the id is missing
watchEffect(() => {
  if (!datasetId.value) {
    alert('Could not get dataset ID')
    router.replace({ name: 'dataset-list' }) // Use a named route for safety
  }
})
</script>

<template>
  <h1>{{ datasetId }}</h1>
</template>

<style lang="css" scoped></style>
