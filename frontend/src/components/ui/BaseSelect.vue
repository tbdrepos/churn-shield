<script setup lang="ts">
import { ref, computed, nextTick, type Directive } from 'vue'
import BaseIcon from './BaseIcon.vue'

type BaseOption = {
  label: string
  value: string | number
}

interface Props<T extends BaseOption> {
  modelValue?: T['value'] | null
  options: T[]
  label?: string
  placeholder?: string
  error?: string
}

const props = withDefaults(defineProps<Props<BaseOption>>(), {
  modelValue: null,
  label: '',
  placeholder: 'Select an option',
  error: '',
})

const emit = defineEmits<{
  'update:modelValue': [value: string | number | null]
  change: [option: BaseOption]
}>()

// State
const isOpen = ref(false)
const activeIndex = ref(-1)
const uuid = `select-${Math.random().toString(36).slice(2)}`
const listboxRef = ref<HTMLUListElement | null>(null)

// Computed
const selectedOption = computed(() => props.options.find((opt) => opt.value === props.modelValue))

const selectedOptionLabel = computed(() => selectedOption.value?.label ?? '')

// Actions
const toggleDropdown = () => {
  isOpen.value = !isOpen.value

  if (isOpen.value) {
    activeIndex.value = props.options.findIndex((opt) => opt.value === props.modelValue)
    if (activeIndex.value === -1) activeIndex.value = 0
  }
}

const closeDropdown = () => {
  isOpen.value = false
  activeIndex.value = -1
}

const selectOption = (index: number) => {
  const option = props.options[index]
  if (option) {
    emit('update:modelValue', option.value)
    emit('change', option)
  }
  closeDropdown()
}

// Keyboard
const onKeyDown = (e: KeyboardEvent) => {
  if (!isOpen.value) {
    if (['ArrowDown', 'Enter', ' '].includes(e.key)) {
      e.preventDefault()
      toggleDropdown()
    }
    return
  }

  switch (e.key) {
    case 'ArrowDown':
      e.preventDefault()
      activeIndex.value = (activeIndex.value + 1) % props.options.length
      scrollToActive()
      break
    case 'ArrowUp':
      e.preventDefault()
      activeIndex.value = (activeIndex.value - 1 + props.options.length) % props.options.length
      scrollToActive()
      break
    case 'Enter':
    case ' ':
      e.preventDefault()
      selectOption(activeIndex.value)
      break
    case 'Escape':
    case 'Tab':
      closeDropdown()
      break
  }
}

const scrollToActive = () => {
  nextTick(() => {
    const el = listboxRef.value?.children[activeIndex.value] as HTMLElement
    el?.scrollIntoView({ block: 'nearest' })
  })
}

// Directive (typed)
type ClickOutsideEl = HTMLElement & {
  __handler__?: (e: Event) => void
}

const vClickOutside: Directive<ClickOutsideEl, () => void> = {
  mounted(el, binding) {
    el.__handler__ = (e: Event) => {
      if (!(el === e.target || el.contains(e.target as Node))) {
        binding.value()
      }
    }
    document.addEventListener('mousedown', el.__handler__)
  },
  unmounted(el) {
    if (el.__handler__) {
      document.removeEventListener('mousedown', el.__handler__)
    }
  },
}
</script>

<template>
  <div class="base-select-container" v-click-outside="closeDropdown">
    <label v-if="label" :for="uuid" class="base-select-label">
      {{ label }}
    </label>

    <div class="base-select-wrapper">
      <div
        :id="uuid"
        class="base-select-display"
        :class="{ 'is-open': isOpen, 'is-error': error }"
        tabindex="0"
        role="combobox"
        aria-haspopup="listbox"
        :aria-expanded="isOpen"
        :aria-controls="`${uuid}-listbox`"
        :aria-labelledby="label ? uuid : undefined"
        @click="toggleDropdown"
        @keydown="onKeyDown"
      >
        <span v-if="!modelValue" class="placeholder">{{ placeholder }}</span>
        <span v-else>{{ selectedOptionLabel }}</span>

        <slot name="icon">
          <span class="chevron" :class="{ rotated: isOpen }" aria-hidden="true">
            <BaseIcon name="ChevronDown" />
          </span>
        </slot>
      </div>

      <transition name="fade">
        <ul
          v-if="isOpen"
          :id="`${uuid}-listbox`"
          ref="listboxRef"
          class="base-select-options"
          role="listbox"
          tabindex="-1"
        >
          <li
            v-for="(option, index) in options"
            :key="String(option.value)"
            :id="`${uuid}-option-${index}`"
            class="base-select-item"
            :class="{
              'is-selected': modelValue === option.value,
              'is-active': activeIndex === index,
            }"
            role="option"
            :aria-selected="modelValue === option.value"
            @click="selectOption(index)"
            @mouseenter="activeIndex = index"
          >
            <slot name="option" :option="option">
              {{ option.label }}
            </slot>
          </li>
          <li v-if="options.length === 0" class="base-select-item no-options" role="presentation">
            No options available
          </li>
        </ul>
      </transition>
    </div>

    <span v-if="error" class="error-message" aria-live="polite">{{ error }}</span>
  </div>
</template>

<style scoped>
.base-select-container {
  display: flex;
  flex-direction: column;
  width: 100%;
  font-family: sans-serif;
}

.base-select-label {
  margin-bottom: 0.5rem;
  font-weight: 600;
  font-size: 0.9rem;
}

.base-select-wrapper {
  position: relative;
}

.base-select-display {
  padding: 12px 15px;
  border: 2px solid var(--gray-300);
  border-radius: 4px;
  background: var(--color-main);
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: border-color 0.2s;
}

.base-select-display.is-open {
  border-color: var(--color-primary);
}

.base-select-display.is-error {
  border-color: var(--color-danger);
}

.placeholder {
  color: var(--gray-500);
}

.chevron {
  font-size: 0.7rem;
  transition: transform 0.3s;
}

.chevron.rotated {
  transform: rotate(180deg);
}

.base-select-options {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  z-index: 10;
  margin: 4px 0 0;
  padding: 0;
  list-style: none;
  background: var(--color-main);
  border: 3px solid var(--color-primary-200);
  border-radius: 4px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  max-height: 200px;
  overflow-y: auto;
}

.base-select-item {
  padding: 10px 15px;
  cursor: pointer;
}

.base-select-item:hover,
.base-select-item.is-active {
  background-color: var(--color-primary-200);
}

.base-select-item.is-selected {
  background-color: var(--color-primary);
  color: var(--color-main);
}

.error-message {
  color: var(--color-danger);
  font-size: 0.8rem;
  margin-top: 4px;
}

/* Transition */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
