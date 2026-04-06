<script setup lang="ts">
import { computed } from 'vue'
import BaseIcon from '@/components/ui/BaseIcon.vue'
import type { ToastType } from '@/stores/toastStore'

const props = defineProps<{
    id: number
    message: string
    type: ToastType
}>()

const emit = defineEmits(['close'])

const iconName = computed(() => {
    const icons: Record<ToastType, string> = {
        success: 'CheckCircle',
        error: 'AlertCircle',
        warning: 'AlertTriangle',
        info: 'Info'
    }
    return icons[props.type]
})
</script>

<template>
    <div :class="['toast', `toast--${type}`]" role="alert">
        <BaseIcon :name="iconName" :size="20" />
        <span class="toast-message">{{ message }}</span>
        <button class="close-btn" @click="emit('close', id)">
            <BaseIcon name="X" :size="16" />
        </button>
    </div>
</template>

<style scoped>
.toast {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 1rem 1.25rem;
    border-radius: 0.5rem;
    background: var(--surface-2-color);
    color: var(--text-color);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    min-width: 300px;
    pointer-events: auto;
}

.toast--success {
    border-left: 4px solid var(--color-success);
}

.toast--error {
    border-left: 4px solid var(--color-danger);
}

.toast--warning {
    border-left: 4px solid var(--color-warning);
}

.toast--info {
    border-left: 4px solid var(--color-primary);
}

.toast-message {
    flex: 1;
    font-size: 0.9rem;
    font-weight: 500;
}

.close-btn {
    background: none;
    border: none;
    cursor: pointer;
    opacity: 0.5;
    transition: opacity 0.2s;
}

.close-btn:hover {
    opacity: 1;
}
</style>