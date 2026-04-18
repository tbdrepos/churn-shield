<script lang="ts" setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useI18n } from 'vue-i18n'
import BaseIcon from '../ui/BaseIcon.vue'

const { t } = useI18n()

// State
const isCollapsed = defineModel({ default: false })
const isMobile = ref(false)
const menuMediaQuery = window.matchMedia('(max-width: 768px)')

// Navigation Data (Keep template clean)
const navGroups = [
  {
    label: 'sidebar.overview',
    items: [
      {
        to: '/app/dashboard',
        icon: 'LayoutDashboard',
        text: 'sidebar.dashboard',
        color: '#8ab4f8',
      },
    ],
  },
  {
    label: 'sidebar.data',
    items: [
      {
        to: '/app/upload',
        icon: 'CloudUpload',
        text: 'sidebar.upload',
        color: '#fdd663',
      },
      {
        to: '/app/datasets',
        icon: 'Database',
        text: 'sidebar.dataset',
        color: '#fdd663',
      },
    ],
  },
  {
    label: 'sidebar.model',
    items: [
      {
        to: '/app/models',
        icon: 'BrainCircuit',
        text: 'sidebar.train',
        color: '#81c995',
      },
      {
        to: '/app/insight',
        icon: 'TrendingUp',
        text: 'sidebar.insight',
        color: '#81c995',
      },
    ],
  },
  {
    label: 'sidebar.customers',
    items: [
      {
        to: '/app/predict',
        icon: 'Users',
        text: 'sidebar.predict',
        color: '#c58af9',
      },
    ],
  },
  {
    label: 'sidebar.account',
    items: [
      {
        to: '/app/account',
        icon: 'Settings',
        text: 'sidebar.settings',
        color: '#f28b82',
      },
    ],
  },
]

function toggleSidebar() {
  isCollapsed.value = !isCollapsed.value
}

function handleMediaQuery(e: MediaQueryListEvent | MediaQueryList) {
  isMobile.value = e.matches
  // On mobile, start hidden. On desktop, start expanded.
  isCollapsed.value = e.matches
}

onMounted(() => {
  handleMediaQuery(menuMediaQuery)
  menuMediaQuery.addEventListener('change', handleMediaQuery)
})

onUnmounted(() => {
  menuMediaQuery.removeEventListener('change', handleMediaQuery)
})
</script>

<template>
  <div v-if="isMobile && !isCollapsed" class="sidebar-overlay" @click="toggleSidebar"></div>

  <aside
    :class="['sidebar', { 'is-collapsed': isCollapsed, 'is-mobile': isMobile }]"
    :aria-expanded="!isCollapsed"
  >
    <div class="sidebar-header">
      <button @click="toggleSidebar" class="toggle-btn" aria-label="Toggle Menu">
        <BaseIcon name="Menu" :stroke-width="3" />
      </button>
    </div>

    <nav class="sidebar-nav">
      <div v-for="group in navGroups" :key="group.label" class="nav-group">
        <p v-if="!isCollapsed" class="group-label">{{ t(group.label) }}</p>

        <RouterLink
          v-for="item in group.items"
          :key="item.to"
          :to="item.to"
          class="nav-link"
          :title="isCollapsed ? t(item.text) : ''"
        >
          <BaseIcon :name="item.icon" :stroke-width="3" />
          <span v-if="!isCollapsed" class="text">{{ t(item.text) }}</span>
        </RouterLink>
      </div>
    </nav>
  </aside>
</template>

<style scoped>
.sidebar {
  width: var(--sidebar-expanded);
  height: 100dvh;
  position: fixed;
  left: 0;
  top: 0;
  transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  flex-direction: column;
  z-index: 1001;
  overflow-x: hidden;
  border: 1px solid var(--gray-300);
}

.sidebar.is-collapsed {
  width: var(--sidebar-collapsed);
}

/* Mobile adjustments */
.sidebar.is-mobile {
  transform: translateX(0);
}
.sidebar.is-mobile.is-collapsed {
  transform: translateX(-100%); /* Hide completely on mobile if collapsed */
  width: var(--sidebar-expanded);
}

.sidebar-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 1000;
}

.sidebar-header {
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 12px;
  gap: 1rem;
}

.toggle-btn {
  background: none;
  border: none;
  color: var(--color-primary);
  font-size: 1.6rem;
  font-weight: 900;
  cursor: pointer;
  border-radius: 50%;
  padding: 0.8rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.toggle-btn:hover {
  background: var(--color-primary-200);
}

.sidebar-nav {
  flex: 1;
  padding: 12px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.group-label {
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--gray-500);
  padding: 1rem;
  margin: 0;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  border-radius: 24px; /* Pill shape like Gemini */
  text-decoration: none;
  color: inherit;
  transition: background 0.2s;
  white-space: nowrap;
}

.nav-link:hover {
  background: var(--gray-300);
}

.nav-link.router-link-active {
  background: var(--gray-700);
  color: #fff;
}

.text {
  font-weight: 700;
}

/* Transitions */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
