<script setup lang="ts">
import { ShieldCheck, Brain, BarChart3, Sparkles } from '@lucide/vue'
import FeatureCard from '@/components/shared/FeatureCard.vue'

const features = [
  {
    title: 'Smart Churn Prediction',
    description: 'Predict customer churn with trained ML models.',
    icon: Brain,
  },
  {
    title: 'Interactive Analytics',
    description: 'Visualize churn trends and feature importance.',
    icon: BarChart3,
  },
  {
    title: 'SHAP Explanations',
    description: 'Understand why predictions were made.',
    icon: Sparkles,
  },
  {
    title: 'Production Security',
    description: 'Role-based authentication and secure APIs.',
    icon: ShieldCheck,
  },
]
</script>

<template>
  <section class="feature-section">
    <strong>Why Churn Shield?</strong>
    <h3>Turn insights into impacts</h3>
    <p>
      Train ML models and generate insights to reduce churn and build stronger customer
      relationships
    </p>
    <div class="feature-cards">
      <FeatureCard
        v-for="feature in features"
        :key="feature.title"
        :title="feature.title"
        :description="feature.description"
        :icon="feature.icon"
      />
    </div>
  </section>
</template>

<style scoped>
.feature-section {
  padding: 1rem;
  margin-bottom: 4rem;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.feature-section strong {
  color: var(--color-primary);
  margin-top: 1rem;
}
.feature-section h3 {
  margin: 0.6rem;
  font-size: 1.8rem;
}
.feature-section p {
  margin: 0;
  padding: 0 0 3rem 0;
  width: 30rem;
  text-align: center;
}
.feature-cards {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 2rem;
}
</style>
