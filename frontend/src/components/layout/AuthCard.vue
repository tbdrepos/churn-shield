<template>
  <main class="auth-page">
    <div class="auth-card">
      <slot name="header"></slot>
      <div class="auth-content">
        <slot></slot>
      </div>
      <slot name="footer"></slot>
    </div>
  </main>
</template>

<style scoped>
.auth-page {
  min-height: 80vh;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 2rem;
}
.auth-card {
  width: 100%;
  max-width: 450px;
  background: var(--surface-1-color);
  padding: 2.5rem;
  border-radius: 1rem;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
}
</style>
