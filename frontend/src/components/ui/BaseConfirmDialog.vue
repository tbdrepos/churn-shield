<script setup lang="ts">
import BaseButton from '@/components/ui/BaseButton.vue'
import BaseIcon from '@/components/ui/BaseIcon.vue'

interface Props {
  reveal: boolean
  title?: string
  message?: string
  confirmText?: string
  cancelText?: string
  variant?: 'danger' | 'primary'
}

withDefaults(defineProps<Props>(), {
  title: 'Are you sure?',
  message: 'This action cannot be undone.',
  confirmText: 'Confirm',
  cancelText: 'Cancel',
  variant: 'primary',
})

const emit = defineEmits(['confirm', 'cancel'])
</script>

<template>
  <Teleport to="body">
    <Transition name="fade">
      <div v-if="reveal" class="modal-overlay" @click="emit('cancel')">
        <div class="modal-content" @click.stop>
          <header class="modal-header">
            <div :class="['icon-box', `icon-box--${variant}`]">
              <BaseIcon :name="variant === 'danger' ? 'AlertTriangle' : 'HelpCircle'" :size="24" />
            </div>
            <h3>{{ title }}</h3>
          </header>

          <div class="modal-body">
            <p>{{ message }}</p>
          </div>

          <footer class="modal-footer">
            <BaseButton variant="secondary" @click="emit('cancel')">
              {{ cancelText }}
            </BaseButton>
            <BaseButton :variant="variant" @click="emit('confirm')">
              {{ confirmText }}
            </BaseButton>
          </footer>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(2px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10000;
}

.modal-content {
  background: white;
  width: 100%;
  max-width: 400px;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
}

.modal-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  text-align: center;
  margin-bottom: 1rem;
}

.icon-box {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.icon-box--danger {
  background: #fce8e8;
  color: var(--color-danger);
}
.icon-box--primary {
  background: #e8f0fe;
  color: var(--color-primary);
}

h3 {
  margin: 0;
  font-size: 1.25rem;
  color: var(--gray-900);
}
p {
  color: var(--gray-500);
  line-height: 1.5;
  text-align: center;
}

.modal-footer {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.75rem;
  margin-top: 1.5rem;
}

/* Animations */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
