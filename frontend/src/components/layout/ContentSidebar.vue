<script lang="ts" setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useI18n } from 'vue-i18n'
const { t } = useI18n()

const isCollapsed = ref(false)
const isMobile = ref(false)

function toggleSidebar() {
  isCollapsed.value = !isCollapsed.value
}

function handleResize() {
  isMobile.value = window.innerWidth < 768
  if (isMobile.value) {
    isCollapsed.value = true
  } else {
    isCollapsed.value = false
  }
}

onMounted(() => {
  // initial size handling
  handleResize()
  // registering event handler in case of resize
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
})
</script>

<template>
  <aside :class="['sidebar', { collapsed: isCollapsed, mobile: isMobile }]">
    <div class="sidebar-header">
      <button v-if="isMobile" @click="toggleSidebar" class="toggle-btn">☰</button>
      <img v-else src="@/assets/logo.png" alt="logo" class="logo" />
    </div>
    <nav v-show="!isCollapsed || !isMobile" class="sidebar-nav">
      {{ t('sidebar.overview') }}
      <RouterLink to="/app/dashboard" class="nav__element"
        >📊{{ t('sidebar.dashboard') }}</RouterLink
      >
      {{ t('sidebar.data') }}
      <RouterLink to="/app/dataset" class="nav__element">🗂{{ t('sidebar.dataset') }}</RouterLink>
      <RouterLink to="/app/upload" class="nav__element">⬆{{ t('sidebar.upload') }}</RouterLink>
      {{ t('sidebar.model') }}
      <RouterLink to="/app/models" class="nav__element">🧠{{ t('sidebar.train') }}</RouterLink>
      <RouterLink to="/app/insight" class="nav__element">📈{{ t('sidebar.insight') }}</RouterLink>
      {{ t('sidebar.customers') }}
      <RouterLink to="/app/predict" class="nav__element">👥{{ t('sidebar.predict') }}</RouterLink>
      {{ t('sidebar.account') }}
      <RouterLink to="/app/account" class="nav__element">⚙{{ t('sidebar.settings') }}</RouterLink>
    </nav>
  </aside>
</template>

<style scoped>
.sidebar {
  width: 250px;
  transition: all 0.3s ease;
  background: #2c3e50;
  color: white;
  height: 100vh;
  position: fixed;
}

.sidebar.collapsed {
  width: 60px;
}

.sidebar.mobile {
  position: absolute;
  z-index: 1000;
}

.sidebar-header {
  display: flex;
  justify-content: start;
  padding: 0 1rem;
}

.toggle-btn {
  background: none;
  border: none;
  color: white;
  font-size: 1.5rem;
  cursor: pointer;
  margin: 1rem 0;
  width: auto;
}

.logo {
  height: 6rem;
  margin-left: 2rem;
  margin-bottom: 4rem;
}

.sidebar-nav {
  display: flex;
  flex-direction: column;
  gap: 0;
  margin: 2rem;
}
.nav__element {
  text-decoration: none;
  color: var(--text-color);
  padding: 0.5rem;
  width: 100%;
}
.nav__element:hover {
  background-color: var(--surface-color);
}
</style>
