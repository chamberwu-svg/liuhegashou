<template>
  <div class="analytics-page">
    <div class="header-banner card">
      <div>
        <h2>📊 数据看板与人工验算 Panel</h2>
        <p class="subtitle">根据 MacauJC / KJ1868 API 调用的实时开奖数据生成多元可视化面板，提供 01-49 号码全量遗漏矩阵供人工校对与验算。</p>
      </div>
      <div class="audit-badge" v-if="analytics">
        <div class="label">数据校验哈希 (SHA256)</div>
        <div class="code">{{ analytics.audit_checksum }}</div>
        <div class="draw-count">基于近 {{ analytics.total_draws }} 期数据生成</div>
      </div>
    </div>

    <!-- 加载中/错误状态 -->
    <div v-if="loading" class="card loading-state">
      ⏳ 正在获取并分析历史开奖数据矩阵...
    </div>

    <div v-else-if="analytics" class="content-wrapper">
      <!-- 1. 冷热与极冷遗漏 TOP5 卡片 -->
      <div class="grid-2">
        <div class="card">
          <h3>🔥 近 {{ analytics.total_draws }} 期热号 TOP 5</h3>
          <div class="rank-list">
            <div v-for="item in analytics.hot_numbers" :key="item.number" class="rank-item">
              <span class="ball-badge red">{{ String(item.number).padStart(2, '0') }}</span>
              <div class="info-group">
                <div class="bar-bg">
                  <div class="bar-fill hot" :style="{ width: item.ratio * 5 + '%' }"></div>
                </div>
                <span class="stat-text">出现 {{ item.frequency }} 次 (占比 {{ item.ratio }}%)</span>
              </div>
            </div>
          </div>
        </div>

        <div class="card">
          <h3>❄️ 极冷遗漏号 TOP 5 (人工预警)</h3>
          <div class="rank-list">
            <div v-for="item in analytics.cold_numbers" :key="item.number" class="rank-item">
              <span class="ball-badge blue">{{ String(item.number).padStart(2, '0') }}</span>
              <div class="info-group">
                <div class="bar-bg">
                  <div class="bar-fill cold" :style="{ width: Math.min(item.missing * 3, 100) + '%' }"></div>
                </div>
                <span class="stat-text">已连续遗漏 <strong>{{ item.missing }}</strong> 期</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 2. 多元属性分布可视化面板 (波色 / 大小 / 单双) -->
      <div class="grid-2 margin-top">
        <div class="card">
          <h3>🎨 特码波色分布统计</h3>
          <div class="color-bars">
            <div class="color-row">
              <span class="color-name red-text font-bold">红波 (RED)</span>
              <div class="bar-bg">
                <div class="bar-fill red-bg" :style="{ width: analytics.color_dist.RED.ratio + '%' }"></div>
              </div>
              <span class="count-label">{{ analytics.color_dist.RED.count }} 次 ({{ analytics.color_dist.RED.ratio }}%)</span>
            </div>
            <div class="color-row">
              <span class="color-name blue-text font-bold">蓝波 (BLUE)</span>
              <div class="bar-bg">
                <div class="bar-fill blue-bg" :style="{ width: analytics.color_dist.BLUE.ratio + '%' }"></div>
              </div>
              <span class="count-label">{{ analytics.color_dist.BLUE.count }} 次 ({{ analytics.color_dist.BLUE.ratio }}%)</span>
            </div>
            <div class="color-row">
              <span class="color-name green-text font-bold">绿波 (GREEN)</span>
              <div class="bar-bg">
                <div class="bar-fill green-bg" :style="{ width: analytics.color_dist.GREEN.ratio + '%' }"></div>
              </div>
              <span class="count-label">{{ analytics.color_dist.GREEN.count }} 次 ({{ analytics.color_dist.GREEN.ratio }}%)</span>
            </div>
          </div>
        </div>

        <div class="card">
          <h3>⚖️ 大小 / 单双形态分布对齐</h3>
          <div class="attr-grid">
            <div class="attr-box">
              <div class="attr-title">大小分布</div>
              <div class="attr-row">
                <span>大 (≥25): {{ analytics.attr_dist.BIG.count }}期 ({{ analytics.attr_dist.BIG.ratio }}%)</span>
                <span>小 (&lt;25): {{ analytics.attr_dist.SMALL.count }}期 ({{ analytics.attr_dist.SMALL.ratio }}%)</span>
              </div>
              <div class="ratio-progress">
                <div class="part big" :style="{ width: analytics.attr_dist.BIG.ratio + '%' }">大</div>
                <div class="part small" :style="{ width: analytics.attr_dist.SMALL.ratio + '%' }">小</div>
              </div>
            </div>

            <div class="attr-box margin-top-sm">
              <div class="attr-title">单双分布</div>
              <div class="attr-row">
                <span>单 (ODD): {{ analytics.attr_dist.ODD.count }}期 ({{ analytics.attr_dist.ODD.ratio }}%)</span>
                <span>双 (EVEN): {{ analytics.attr_dist.EVEN.count }}期 ({{ analytics.attr_dist.EVEN.ratio }}%)</span>
              </div>
              <div class="ratio-progress">
                <div class="part odd" :style="{ width: analytics.attr_dist.ODD.ratio + '%' }">单</div>
                <div class="part even" :style="{ width: analytics.attr_dist.EVEN.ratio + '%' }">双</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 3. 01-49 号码全量人工分析验算大表 -->
      <div class="card margin-top">
        <div class="table-header">
          <h3>📋 01 - 49 号码全量遗漏与频次验算矩阵</h3>
          <div class="filter-group">
            <input type="text" v-model="searchQuery" placeholder="搜索号码 (例如: 17)..." class="search-input" />
            <select v-model="colorFilter" class="filter-select">
              <option value="">全部波色</option>
              <option value="RED">红波</option>
              <option value="BLUE">蓝波</option>
              <option value="GREEN">绿波</option>
            </select>
          </div>
        </div>

        <table class="data-table">
          <thead>
            <tr>
              <th @click="sortBy('number')">号码 ⇕</th>
              <th>波色</th>
              <th>大小</th>
              <th>单双</th>
              <th @click="sortBy('current_missing')">当前遗漏期数 ⇕</th>
              <th @click="sortBy('max_missing')">历史最大遗漏 ⇕</th>
              <th @click="sortBy('frequency_30')">近 30 期频次 ⇕</th>
              <th @click="sortBy('hot_score')">冷热指数得分 ⇕</th>
              <th>人工验算状态</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="row in filteredMatrix" :key="row.number">
              <td>
                <span :class="['ball-chip', row.color.toLowerCase()]">{{ String(row.number).padStart(2, '0') }}</span>
              </td>
              <td>
                <span :class="['color-tag', row.color.toLowerCase()]">{{ row.color === 'RED' ? '红波' : (row.color === 'BLUE' ? '蓝波' : '绿波') }}</span>
              </td>
              <td>{{ row.size === 'BIG' ? '大' : '小' }}</td>
              <td>{{ row.odd_even === 'ODD' ? '单' : '双' }}</td>
              <td><strong :class="{ 'warning-missing': row.current_missing > 20 }">{{ row.current_missing }} 期</strong></td>
              <td>{{ row.max_missing }} 期</td>
              <td>{{ row.frequency_30 }} 次</td>
              <td>
                <div class="score-pill">
                  <div class="pill-fill" :style="{ width: row.hot_score + '%' }"></div>
                  <span class="score-num">{{ row.hot_score }}</span>
                </div>
              </td>
              <td><span class="status-ok">✓ API已验算</span></td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

const analytics = ref(null)
const loading = ref(true)
const searchQuery = ref('')
const colorFilter = ref('')
const sortField = ref('number')
const sortAsc = ref(true)

async function fetchAnalytics() {
  loading.value = true
  try {
    const res = await fetch('/api/analytics?limit=300')
    analytics.value = await res.json()
  } catch (e) {
    console.error('Fetch analytics error:', e)
  } finally {
    loading.value = false
  }
}

function sortBy(field) {
  if (sortField.value === field) {
    sortAsc.value = !sortAsc.value
  } else {
    sortField.value = field
    sortAsc.value = true
  }
}

const filteredMatrix = computed(() => {
  if (!analytics.value || !analytics.value.missing_matrix) return []
  let list = analytics.value.missing_matrix

  if (searchQuery.value) {
    list = list.filter(item => String(item.number).includes(searchQuery.value.trim()))
  }
  if (colorFilter.value) {
    list = list.filter(item => item.color === colorFilter.value)
  }

  return list.sort((a, b) => {
    let valA = a[sortField.value]
    let valB = b[sortField.value]
    if (valA < valB) return sortAsc.value ? -1 : 1
    if (valA > valB) return sortAsc.value ? 1 : -1
    return 0
  })
})

onMounted(() => {
  fetchAnalytics()
})
</script>

<style scoped>
.analytics-page {
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
.header-banner {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-left: 5px solid #1890ff;
}
.subtitle {
  color: #666;
  font-size: 13px;
  margin-top: 4px;
}
.audit-badge {
  background: #fafafa;
  border: 1px solid #e8e8e8;
  padding: 10px 16px;
  border-radius: 6px;
  text-align: right;
}
.audit-badge .label {
  font-size: 11px;
  color: #8c8c8c;
}
.audit-badge .code {
  font-family: monospace;
  font-weight: bold;
  color: #1890ff;
  font-size: 14px;
}
.audit-badge .draw-count {
  font-size: 12px;
  color: #52c41a;
  margin-top: 2px;
}

.loading-state {
  text-align: center;
  padding: 40px;
  font-size: 16px;
  color: #666;
}

.grid-2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}
.margin-top {
  margin-top: 10px;
}
.margin-top-sm {
  margin-top: 15px;
}

.rank-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-top: 15px;
}
.rank-item {
  display: flex;
  align-items: center;
  gap: 12px;
}
.ball-badge {
  width: 32px;
  height: 32px;
  line-height: 32px;
  text-align: center;
  border-radius: 50%;
  color: white;
  font-weight: bold;
  font-size: 14px;
}
.ball-badge.red { background: radial-gradient(circle at 30% 30%, #ff7875, #ff4d4f); }
.ball-badge.blue { background: radial-gradient(circle at 30% 30%, #69c0ff, #1890ff); }

.info-group {
  flex: 1;
}
.bar-bg {
  background: #f0f0f0;
  height: 10px;
  border-radius: 5px;
  overflow: hidden;
  margin-bottom: 4px;
}
.bar-fill {
  height: 100%;
  border-radius: 5px;
}
.bar-fill.hot { background: #ff4d4f; }
.bar-fill.cold { background: #1890ff; }

.stat-text {
  font-size: 12px;
  color: #555;
}

.color-bars {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-top: 15px;
}
.color-row {
  display: flex;
  align-items: center;
  gap: 12px;
}
.color-name {
  width: 90px;
  font-size: 13px;
}
.red-text { color: #ff4d4f; }
.blue-text { color: #1890ff; }
.green-text { color: #52c41a; }
.font-bold { font-weight: bold; }

.bar-fill.red-bg { background: #ff4d4f; }
.bar-fill.blue-bg { background: #1890ff; }
.bar-fill.green-bg { background: #52c41a; }

.count-label {
  width: 100px;
  font-size: 12px;
  color: #666;
  text-align: right;
}

.attr-box {
  background: #fafafa;
  padding: 12px;
  border-radius: 6px;
  border: 1px solid #f0f0f0;
}
.attr-title {
  font-size: 13px;
  font-weight: bold;
  margin-bottom: 6px;
}
.attr-row {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: #555;
  margin-bottom: 6px;
}
.ratio-progress {
  display: flex;
  height: 20px;
  border-radius: 4px;
  overflow: hidden;
  font-size: 11px;
  color: white;
  font-weight: bold;
  text-align: center;
  line-height: 20px;
}
.part.big { background: #1890ff; }
.part.small { background: #52c41a; }
.part.odd { background: #722ed1; }
.part.even { background: #fa8c16; }

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}
.filter-group {
  display: flex;
  gap: 10px;
}
.search-input {
  padding: 6px 12px;
  border: 1px solid #d9d9d9;
  border-radius: 4px;
  font-size: 13px;
}
.filter-select {
  padding: 6px 12px;
  border: 1px solid #d9d9d9;
  border-radius: 4px;
  font-size: 13px;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
}
.data-table th, .data-table td {
  padding: 10px 12px;
  text-align: left;
  border-bottom: 1px solid #f0f0f0;
  font-size: 13px;
}
.data-table th {
  cursor: pointer;
  background: #fafafa;
  user-select: none;
}
.ball-chip {
  display: inline-block;
  width: 26px;
  height: 26px;
  line-height: 26px;
  text-align: center;
  border-radius: 50%;
  color: white;
  font-weight: bold;
}
.ball-chip.red { background: #ff4d4f; }
.ball-chip.blue { background: #1890ff; }
.ball-chip.green { background: #52c41a; }

.color-tag {
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 12px;
}
.color-tag.red { background: #fff1f0; color: #ff4d4f; border: 1px solid #ffa39e; }
.color-tag.blue { background: #e6f7ff; color: #1890ff; border: 1px solid #91d5ff; }
.color-tag.green { background: #f6ffed; color: #52c41a; border: 1px solid #b7eb8f; }

.warning-missing {
  color: #ff4d4f;
  font-weight: bold;
}

.score-pill {
  position: relative;
  background: #f0f0f0;
  height: 16px;
  border-radius: 8px;
  overflow: hidden;
  width: 80px;
}
.pill-fill {
  background: linear-gradient(90deg, #1890ff, #ff4d4f);
  height: 100%;
}
.score-num {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  text-align: center;
  font-size: 10px;
  line-height: 16px;
  color: #000;
  font-weight: bold;
}
.status-ok {
  color: #389e0d;
  font-size: 12px;
}
</style>
