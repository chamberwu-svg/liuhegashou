<template>
  <div class="dashboard-page">
    <h2>🎯 预测中心仪表盘 Dashboard</h2>
    <div class="sync-banner">
      <button @click="syncData" class="btn primary" :disabled="syncing">
        {{ syncing ? '正在从澳门马会 / KJ1868 API 同步数据...' : '⚡ 一键同步最新开奖数据 (MacauJC/KJ1868 API)' }}
      </button>
      <span v-if="syncMsg" class="sync-msg">{{ syncMsg }}</span>
    </div>

    <div class="grid-2">
      <PredictionRanking :rankings="rankings" />
      <ConsensusChart :rankings="rankings" />
    </div>

    <div class="grid-2 margin-top">
      <ModelScore />
      <BacktestTable :backtestData="backtestData" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import PredictionRanking from '../components/PredictionRanking.vue'
import ModelScore from '../components/ModelScore.vue'
import ConsensusChart from '../components/ConsensusChart.vue'
import BacktestTable from '../components/BacktestTable.vue'

const rankings = ref([])
const backtestData = ref({})
const syncing = ref(false)
const syncMsg = ref('')

async function fetchPrediction() {
  try {
    const res = await fetch('/api/predict')
    const data = await res.json()
    if (data.ranking) {
      rankings.value = data.ranking
    }
  } catch (e) {
    console.error('Fetch predict error:', e)
  }
}

async function fetchBacktest() {
  try {
    const res = await fetch('/api/backtest')
    const data = await res.json()
    backtestData.value = data
  } catch (e) {
    console.error('Fetch backtest error:', e)
  }
}

async function syncData() {
  syncing.value = true
  syncMsg.value = ''
  try {
    const res = await fetch('/api/sync', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ limit: 100 })
    })
    const data = await res.json()
    syncMsg.value = data.message || '数据同步完成！'
    await fetchPrediction()
    await fetchBacktest()
  } catch (e) {
    syncMsg.value = '同步失败或使用本地数据。'
  } finally {
    syncing.value = false
  }
}

onMounted(() => {
  fetchPrediction()
  fetchBacktest()
})
</script>

<style scoped>
.dashboard-page {
  display: flex;
  flex-direction: column;
  gap: 20px;
}
.sync-banner {
  background: white;
  padding: 16px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 15px;
}
.btn {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
}
.btn.primary {
  background: #1890ff;
  color: white;
}
.btn:disabled {
  background: #ccc;
  cursor: not-allowed;
}
.sync-msg {
  color: #52c41a;
  font-size: 14px;
}
.grid-2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}
.margin-top {
  margin-top: 10px;
}
</style>
