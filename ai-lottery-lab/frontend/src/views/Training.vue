<template>
  <div class="training-page">
    <h2>⚙️ AI 模型训练控制台 Training</h2>
    <div class="card">
      <div class="form-group">
        <label>数据范围 (历史期数)：</label>
        <select v-model="datasetSize">
          <option value="100">最近 100 期</option>
          <option value="300">最近 300 期</option>
          <option value="500">最近 500 期</option>
          <option value="1000">最近 1000 期</option>
        </select>
      </div>

      <div class="form-group">
        <label>选择参与训练的模型：</label>
        <div class="checkbox-group">
          <label><input type="checkbox" value="markov" v-model="selectedModels" /> 马尔可夫链 (Markov)</label>
          <label><input type="checkbox" value="bayes" v-model="selectedModels" /> 贝叶斯模型 (Bayesian)</label>
          <label><input type="checkbox" value="rf" v-model="selectedModels" /> 随机森林 (Random Forest)</label>
          <label><input type="checkbox" value="xgb" v-model="selectedModels" /> XGBoost</label>
          <label><input type="checkbox" value="lgb" v-model="selectedModels" /> LightGBM</label>
          <label><input type="checkbox" value="lstm" v-model="selectedModels" /> LSTM 神经网络</label>
        </div>
      </div>

      <button @click="startTraining" class="btn primary" :disabled="training">
        {{ training ? '🚀 AI 训练计算中...' : '▶ 开始多模型训练' }}
      </button>

      <div v-if="trainResult" class="result-box">
        <h4>训练完成结果报告：</h4>
        <pre>{{ JSON.stringify(trainResult, null, 2) }}</pre>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const datasetSize = ref('500')
const selectedModels = ref(['markov', 'bayes', 'rf', 'xgb', 'lgb', 'lstm'])
const training = ref(false)
const trainResult = ref(null)

async function startTraining() {
  training.value = true
  trainResult.value = null
  try {
    const res = await fetch('/api/train', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        dataset: datasetSize.value,
        models: selectedModels.value
      })
    })
    trainResult.value = await res.json()
  } catch (e) {
    trainResult.value = { error: '训练发生异常: ' + e.message }
  } finally {
    training.value = false
  }
}
</script>

<style scoped>
.training-page {
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
.form-group {
  margin-bottom: 20px;
}
.form-group label {
  display: block;
  font-weight: bold;
  margin-bottom: 8px;
}
select {
  padding: 8px 12px;
  border-radius: 4px;
  border: 1px solid #ccc;
  width: 200px;
}
.checkbox-group {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 12px;
}
.btn {
  padding: 10px 24px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
}
.btn.primary {
  background: #52c41a;
  color: white;
}
.result-box {
  margin-top: 20px;
  background: #fafafa;
  padding: 16px;
  border-radius: 6px;
  border: 1px solid #e8e8e8;
}
pre {
  margin: 0;
  font-family: monospace;
}
</style>
