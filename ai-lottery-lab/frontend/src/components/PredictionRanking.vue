<template>
  <div class="component-card">
    <h3>🏆 AI 特码预测 Top 10 综合排名</h3>
    <table class="data-table">
      <thead>
        <tr>
          <th>排名</th>
          <th>号码</th>
          <th>综合评分</th>
          <th>模型支持度</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(item, index) in rankings" :key="item.number">
          <td>#{{ index + 1 }}</td>
          <td><span class="number-badge">{{ String(item.number).padStart(2, '0') }}</span></td>
          <td><strong>{{ item.score }}</strong></td>
          <td><span class="consensus-badge">{{ item.consensus }}</span></td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
defineProps({
  rankings: {
    type: Array,
    default: () => []
  }
})
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
  margin-top: 10px;
}
.data-table th, .data-table td {
  padding: 10px 12px;
  text-align: left;
  border-bottom: 1px solid #f0f0f0;
}
.number-badge {
  display: inline-block;
  background: #e6f7ff;
  color: #1890ff;
  font-weight: bold;
  padding: 2px 8px;
  border-radius: 4px;
}
.consensus-badge {
  background: #f6ffed;
  color: #52c41a;
  padding: 2px 6px;
  border-radius: 4px;
  font-weight: 500;
}
</style>
