<script setup lang="ts">
import { computed, type Component } from 'vue'
import * as icons from '@lucide/vue'

const props = defineProps<{
    name: string
    size?: number
    color?: string
    strokeWidth?: number
}>()

const iconComponent = computed(() => {
    // 1. Safeguard: avoid returning the base Icon component or helpers
    if (props.name === 'Icon' || props.name === 'createLucideIcon') {
        return icons.HelpCircle as Component
    }

    // 2. Resolve the icon PascalCase (e.g., 'mail' -> 'Mail')
    const iconName = props.name.charAt(0).toUpperCase() + props.name.slice(1)
    const icon = icons[iconName as keyof typeof icons]

    // 3. Cast as Component to bypass the internal prop validation error
    return (icon || icons.HelpCircle) as Component
})
</script>

<template>
    <component :is="iconComponent" :size="size ?? 20" :stroke-width="strokeWidth ?? 2" :color="color ?? 'currentColor'"
        class="base-icon" />
</template>



<style scoped>
.base-icon {
    display: inline-block;
    vertical-align: middle;
    flex-shrink: 0;
    /* Prevents icon from squishing in flex containers */
}
</style>