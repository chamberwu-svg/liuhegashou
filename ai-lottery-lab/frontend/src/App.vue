<template>
  <div class="app-layout">
    <header class="app-header">
      <div class="header-title">🧪 AI 预测实验室 AI Lottery Prediction Lab</div>
      <nav class="nav-menu">
        <button
          v-for="tab in tabs"
          :key="tab.id"
          :class="['nav-btn', { active: currentTab === tab.id }]"
          @click="currentTab = tab.id"
        >
          {{ tab.name }}
        </button>
      </nav>
    </header>

    <main class="app-content">
      <Dashboard v-if="currentTab === 'dashboard'" />
      <Training v-else-if="currentTab === 'training'" />
      <Models v-else-if="currentTab === 'models'" />
      <Backtest v-else-if="currentTab === 'backtest'" />
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import Dashboard from './views/Dashboard.vue'
import Training from './views/Training.vue'
import Models from './views/Models.vue'
import Backtest from './views/Backtest.vue'

const currentTab = ref('dashboard')

const tabs = [
  { id: 'dashboard', name: '📊 预测中心 Dashboard' },
  { id: 'training', name: '⚙️ 模型训练 Training' },
  { id: 'models', name: '🔬 模型分析 Models' },
  { id: 'backtest', name: '📜 历史回测 Backtest' }
]
</script>

<style>
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}
body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  background-color: #f4f6f8;
  color: #333;
}
.app-layout {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}
.app-header {
  background: white;
  padding: 16px 24px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}
.header-title {
  font-size: 20px;
  font-weight: bold;
  color: #1890ff;
}
.nav-menu {
  display: flex;
  gap: 10px;
}
.nav-btn {
  padding: 8px 16px;
  border: 1px solid #d9d9d9;
  background: white;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.2s;
}
.nav-btn:hover {
  color: #1890ff;
  border-color: #1890ff;
}
.nav-btn.active {
  background: #1890ff;
  color: white;
  border-color: #1890ff;
}
.app-content {
  min-height: 500px;
}
</style>
