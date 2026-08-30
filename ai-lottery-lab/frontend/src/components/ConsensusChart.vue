<template>
  <div class="component-card">
    <h3>🤝 模型一致性 (Consensus Index)</h3>
    <div class="consensus-list">
      <div v-for="item in consensusData" :key="item.number" class="consensus-row">
        <span class="num">号码 {{ String(item.number).padStart(2, '0') }}</span>
        <div class="bar-container">
          <div class="bar" :style="{ width: item.percentage + '%' }"></div>
        </div>
        <span class="support">{{ item.consensus }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  rankings: {
    type: Array,
    default: () => []
  }
})

const consensusData = computed(() => {
  return props.rankings.slice(0, 5).map(item => {
    const parts = (item.consensus || "5/6").split('/')
    const count = parseInt(parts[0]) || 5
    const total = parseInt(parts[1]) || 6
    return {
      number: item.number,
      consensus: item.consensus,
      percentage: (count / total) * 100
    }
  })
})
</script>

<style scoped>
.component-card {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}
.consensus-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-top: 15px;
}
.consensus-row {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 14px;
}
.num {
  width: 70px;
  font-weight: 500;
}
.bar-container {
  flex: 1;
  background: #f5f5f5;
  height: 14px;
  border-radius: 7px;
  overflow: hidden;
}
.bar {
  background: linear-gradient(90deg, #52c41a, #1890ff);
  height: 100%;
  border-radius: 7px;
}
.support {
  width: 40px;
  text-align: right;
  font-weight: bold;
}
</style>
