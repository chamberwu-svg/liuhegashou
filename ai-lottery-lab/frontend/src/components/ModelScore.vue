<template>
  <div class="component-card">
    <h3>📊 模型得分对比与权重</h3>
    <div class="model-list">
      <div v-for="model in models" :key="model.name" class="model-item">
        <div class="model-header">
          <span>{{ model.name }}</span>
          <span>权重: {{ (model.weight * 100).toFixed(0) }}%</span>
        </div>
        <div class="progress-bg">
          <div class="progress-fill" :style="{ width: model.score + '%' }"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const models = [
  { name: 'Markov (马尔可夫)', weight: 0.10, score: 82 },
  { name: 'Bayesian (贝叶斯)', weight: 0.15, score: 94 },
  { name: 'Random Forest (随机森林)', weight: 0.15, score: 91 },
  { name: 'XGBoost', weight: 0.20, score: 96 },
  { name: 'LightGBM', weight: 0.20, score: 93 },
  { name: 'LSTM (深度学习)', weight: 0.20, score: 89 }
]
</script>

<style scoped>
.component-card {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}
.model-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-top: 15px;
}
.model-header {
  display: flex;
  justify-content: space-between;
  font-size: 14px;
  margin-bottom: 4px;
}
.progress-bg {
  background: #f0f0f0;
  height: 8px;
  border-radius: 4px;
  overflow: hidden;
}
.progress-fill {
  background: #1890ff;
  height: 100%;
  border-radius: 4px;
}
</style>
