<template>
  <div class="models-page">
    <h2>🔬 6 大模型原理与输出分析 Models</h2>
    <div class="models-grid">
      <div v-for="m in modelDetails" :key="m.id" class="model-card">
        <div class="card-header">
          <h3>{{ m.name }}</h3>
          <span class="badge">{{ m.type }}</span>
        </div>
        <p class="desc">{{ m.description }}</p>
        <div class="details">
          <div><strong>关键算法：</strong> {{ m.algorithm }}</div>
          <div><strong>特征输入：</strong> {{ m.features }}</div>
          <div><strong>独立概率输出：</strong> 01 ～ 49 维向量</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const modelDetails = [
  { id: 'markov', name: '马尔可夫链 (Markov)', type: '状态转移统计', algorithm: '1阶/2阶/3阶 Markov Chain', description: '分析上一期特码转移至下一期各号码的条件转移概率。', features: '上一期/前N期特码序列' },
  { id: 'bayes', name: '贝叶斯模型 (Bayesian)', type: '后验概率更新', algorithm: 'Bayes Theorem (Prior × Evidence)', description: '结合历史先验分布与近期出现频率、遗漏值更新后验得分。', features: '历史频次、近100期频次、当前遗漏' },
  { id: 'rf', name: '随机森林 (Random Forest)', type: '集成决策树', algorithm: 'RandomForestClassifier', description: '构建多棵决策树降低方差，对高维结构化遗漏特征进行分类打分。', features: '196维特征（冷热/遗漏/间隔/波色/单双）' },
  { id: 'xgb', name: 'XGBoost', type: '梯度提升树', algorithm: 'XGBClassifier', description: '高精度梯度提升树模型，适合结构化开奖特征。', features: '196维多指标特征向量' },
  { id: 'lgb', name: 'LightGBM', type: '轻量梯度提升树', algorithm: 'LGBMClassifier', description: '基于直方图算法的高效 GBDT 模型，与 XGBoost 并行预测。', features: '196维多指标特征向量' },
  { id: 'lstm', name: 'LSTM 神经网络', type: '深度时序网络', algorithm: 'PyTorch LSTM (Embedding + Dense)', description: '对历史开奖序列构建滑动时序窗口（20/30/50/100期），捕捉长期依赖。', features: 'Sequence Tensor (Batch, Seq_Len, Embed_Dim)' }
]
</script>

<style scoped>
.models-page {
  display: flex;
  flex-direction: column;
  gap: 20px;
}
.models-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}
.model-card {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #f0f0f0;
  padding-bottom: 10px;
}
.badge {
  background: #e6f7ff;
  color: #1890ff;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
}
.desc {
  color: #666;
  margin: 12px 0;
  font-size: 14px;
}
.details {
  font-size: 13px;
  display: flex;
  flex-direction: column;
  gap: 6px;
  background: #fafafa;
  padding: 10px;
  border-radius: 4px;
}
</style>
