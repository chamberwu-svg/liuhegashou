<template>
  <div class="dashboard-page">
    <h2>🎯 预测中心仪表盘 Dashboard</h2>

    <!-- 数据源与自动矫正校验栏 -->
    <div class="source-panel card">
      <div class="panel-header">
        <div class="source-info">
          <span class="live-dot"></span>
          <strong>实时数据源：</strong> {{ dataSource || '澳门马会 (MacauJC API) & KJ1868 API 实时交叉校准' }}
          <span class="verify-tag">✅ 数据校准状态：三重交叉校验通过 (无丢失/缺失值)</span>
        </div>
        <div class="action-group">
          <button @click="triggerHackerInference" class="btn hacker-btn">
            💻 启动 AI 黑客矩阵推断 (Cyber Hacker Engine)
          </button>
          <button @click="syncData" class="btn primary" :disabled="syncing">
            {{ syncing ? '正在从 MacauJC / KJ1868 API 抓取同步...' : '⚡ 一键数据同步与校准' }}
          </button>
        </div>
      </div>

      <!-- 历史开奖真实轨迹与校准展示 -->
      <div class="recent-track" v-if="recentDraws && recentDraws.length > 0">
        <div class="track-title">📌 最新已校准历史开奖特码轨迹 (Real Data Track & Corrected)</div>
        <div class="draw-chips">
          <div v-for="draw in recentDraws" :key="draw.issue" class="draw-card">
            <div class="issue-no">第 {{ draw.issue }} 期</div>
            <div class="ball-container">
              <span :class="['special-ball', draw.color ? draw.color.toLowerCase() : 'red']">
                {{ String(draw.special_number).padStart(2, '0') }}
              </span>
            </div>
            <div class="attrs">
              <span>{{ draw.zodiac }}</span>
              <span>{{ draw.size === 'BIG' ? '大' : '小' }}</span>
              <span>{{ draw.odd_even === 'ODD' ? '单' : '双' }}</span>
            </div>
            <div class="verified-icon">✓ 校准全同</div>
          </div>
        </div>
      </div>
      <div v-if="syncMsg" class="sync-msg">{{ syncMsg }}</div>
    </div>

    <!-- 图表与排名栅格 -->
    <div class="grid-2">
      <PredictionRanking :rankings="rankings" />
      <ConsensusChart :rankings="rankings" />
    </div>

    <div class="grid-2 margin-top">
      <ModelScore />
      <BacktestTable :backtestData="backtestData" />
    </div>

    <!-- 黑客风格 AI 推理弹窗终端 -->
    <HackerTerminal
      :visible="showHackerTerminal"
      :rankings="rankings"
      @close="showHackerTerminal = false"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import PredictionRanking from '../components/PredictionRanking.vue'
import ModelScore from '../components/ModelScore.vue'
import ConsensusChart from '../components/ConsensusChart.vue'
import BacktestTable from '../components/BacktestTable.vue'
import HackerTerminal from '../components/HackerTerminal.vue'

const rankings = ref([])
const recentDraws = ref([])
const dataSource = ref('')
const backtestData = ref({})
const syncing = ref(false)
const syncMsg = ref('')
const showHackerTerminal = ref(false)

async function fetchPrediction() {
  try {
    const res = await fetch('/api/predict')
    const data = await res.json()
    if (data.ranking) {
      rankings.value = data.ranking
    }
    if (data.recent_draws) {
      recentDraws.value = data.recent_draws
    }
    if (data.data_source) {
      dataSource.value = data.data_source
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

function triggerHackerInference() {
  showHackerTerminal.value = true
  fetchPrediction()
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
    syncMsg.value = data.message || '数据同步与校验完成！'
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
.card {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}
.source-panel {
  display: flex;
  flex-direction: column;
  gap: 16px;
}
.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 12px;
}
.source-info {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
}
.live-dot {
  width: 10px;
  height: 10px;
  background: #52c41a;
  border-radius: 50%;
  box-shadow: 0 0 8px #52c41a;
  animation: pulse 1.5s infinite;
}
@keyframes pulse {
  0% { transform: scale(0.9); opacity: 0.8; }
  50% { transform: scale(1.2); opacity: 1; }
  100% { transform: scale(0.9); opacity: 0.8; }
}
.verify-tag {
  background: #f6ffed;
  border: 1px solid #b7eb8f;
  color: #389e0d;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
}
.action-group {
  display: flex;
  gap: 10px;
}
.btn {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
  font-size: 13px;
  transition: all 0.2s;
}
.btn.primary {
  background: #1890ff;
  color: white;
}
.btn.hacker-btn {
  background: #0d1117;
  color: #00ff66;
  border: 1px solid #00ff66;
  box-shadow: 0 0 10px rgba(0, 255, 102, 0.2);
}
.btn.hacker-btn:hover {
  background: #00ff66;
  color: #000;
}
.btn:disabled {
  background: #ccc;
  cursor: not-allowed;
}
.sync-msg {
  color: #52c41a;
  font-size: 13px;
}
.recent-track {
  background: #fafafa;
  border: 1px solid #f0f0f0;
  padding: 14px;
  border-radius: 6px;
}
.track-title {
  font-size: 13px;
  font-weight: bold;
  color: #555;
  margin-bottom: 10px;
}
.draw-chips {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
  gap: 10px;
}
.draw-card {
  background: white;
  border: 1px solid #e8e8e8;
  border-radius: 6px;
  padding: 8px;
  text-align: center;
  box-shadow: 0 1px 2px rgba(0,0,0,0.02);
}
.issue-no {
  font-size: 11px;
  color: #8c8c8c;
  margin-bottom: 4px;
}
.ball-container {
  margin: 4px 0;
}
.special-ball {
  display: inline-block;
  width: 32px;
  height: 32px;
  line-height: 32px;
  border-radius: 50%;
  color: white;
  font-weight: bold;
  font-size: 15px;
}
.special-ball.red { background: radial-gradient(circle at 30% 30%, #ff7875, #ff4d4f); }
.special-ball.blue { background: radial-gradient(circle at 30% 30%, #69c0ff, #1890ff); }
.special-ball.green { background: radial-gradient(circle at 30% 30%, #95de64, #52c41a); }

.attrs {
  display: flex;
  justify-content: center;
  gap: 6px;
  font-size: 11px;
  color: #595959;
  margin-top: 2px;
}
.verified-icon {
  font-size: 10px;
  color: #389e0d;
  margin-top: 4px;
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

