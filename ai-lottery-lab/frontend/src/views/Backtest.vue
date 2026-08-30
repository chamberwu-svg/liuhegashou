<template>
  <div class="backtest-page">
    <h2>📜 自动回测与性能评价 Backtest</h2>
    <div class="card">
      <div class="controls">
        <label>回测窗口大小：</label>
        <select v-model="backtestPeriod">
          <option value="100">历史 100 期</option>
          <option value="300">历史 300 期</option>
          <option value="500">历史 500 期</option>
          <option value="1000">历史 1000 期</option>
        </select>
        <button @click="runBacktest" class="btn primary" :disabled="loading">
          {{ loading ? '⏳ 正在计算 Walk-Forward 逐期滚动回测...' : '▶ 执行 Walk-Forward 回测' }}
        </button>
      </div>

      <div class="results-grid" v-if="metrics">
        <div class="metric-card">
          <div class="title">Top 1 命中率</div>
          <div class="value">{{ formatPercent(metrics.top1) }}</div>
        </div>
        <div class="metric-card">
          <div class="title">Top 5 命中率</div>
          <div class="value highlight">{{ formatPercent(metrics.top5) }}</div>
        </div>
        <div class="metric-card">
          <div class="title">Top 10 命中率</div>
          <div class="value">{{ formatPercent(metrics.top10) }}</div>
        </div>
        <div class="metric-card">
          <div class="title">随机概率基准</div>
          <div class="value sub">{{ formatPercent(metrics.random_baseline || 0.0204) }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const backtestPeriod = ref('500')
const loading = ref(false)
const metrics = ref(null)

async function runBacktest() {
  loading.value = true
  try {
    const res = await fetch('/api/backtest')
    metrics.value = await res.json()
  } catch (e) {
    console.error('Run backtest error:', e)
  } finally {
    loading.value = false
  }
}

function formatPercent(val) {
  if (val === undefined || val === null) return '0.0%'
  return (val * 100).toFixed(2) + '%'
}

onMounted(() => {
  runBacktest()
})
</script>

<style scoped>
.backtest-page {
  display: flex;
  flex-direction: column;
  gap: 20px;
}
.card {
  background: white;
  padding: 24px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}
.controls {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 24px;
}
select {
  padding: 8px 12px;
  border-radius: 4px;
  border: 1px solid #ccc;
}
.btn {
  padding: 8px 18px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
}
.btn.primary {
  background: #1890ff;
  color: white;
}
.results-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}
.metric-card {
  background: #fafafa;
  padding: 16px;
  border-radius: 6px;
  border: 1px solid #f0f0f0;
  text-align: center;
}
.title {
  font-size: 14px;
  color: #666;
  margin-bottom: 8px;
}
.value {
  font-size: 24px;
  font-weight: bold;
  color: #333;
}
.value.highlight {
  color: #52c41a;
}
.value.sub {
  color: #8c8c8c;
}
</style>
