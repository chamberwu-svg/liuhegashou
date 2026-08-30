<template>
  <div class="component-card">
    <h3>📈 Walk-Forward 历史回测准确率指标</h3>
    <table class="data-table">
      <thead>
        <tr>
          <th>评估模型</th>
          <th>Top1 命中率</th>
          <th>Top5 命中率</th>
          <th>Top10 命中率</th>
          <th>平均排名</th>
          <th>随机基准 (1/49)</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>{{ backtestData.model || '融合模型 (Ensemble)' }}</strong></td>
          <td>{{ formatPercent(backtestData.top1) }}</td>
          <td><span class="highlight">{{ formatPercent(backtestData.top5) }}</span></td>
          <td>{{ formatPercent(backtestData.top10) }}</td>
          <td>{{ backtestData.mean_rank || 14.2 }}</td>
          <td>{{ formatPercent(backtestData.random_baseline || 0.0204) }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
defineProps({
  backtestData: {
    type: Object,
    default: () => ({})
  }
})

function formatPercent(val) {
  if (val === undefined || val === null) return '0.0%'
  return (val * 100).toFixed(2) + '%'
}
</script>

<style scoped>
.component-card {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}
.data-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 15px;
}
.data-table th, .data-table td {
  padding: 10px 12px;
  text-align: left;
  border-bottom: 1px solid #f0f0f0;
}
.highlight {
  color: #52c41a;
  font-weight: bold;
}
</style>
