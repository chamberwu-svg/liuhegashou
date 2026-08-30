<template>
  <div class="hacker-terminal-overlay" v-if="visible">
    <div class="terminal-box">
      <div class="terminal-header">
        <div class="window-buttons">
          <span class="dot red"></span>
          <span class="dot yellow"></span>
          <span class="dot green"></span>
        </div>
        <div class="terminal-title">🤖 AI-LOTTERY-LAB // CYBER MATRIX INFERENCE ENGINE</div>
        <button class="close-btn" @click="closeTerminal">✕ ESC</button>
      </div>

      <div class="terminal-body" ref="terminalBody">
        <div class="matrix-bg"></div>
        <div class="log-line" v-for="(log, index) in logs" :key="index" :class="log.type">
          <span class="timestamp">[{{ log.time }}]</span>
          <span class="prefix">&gt;</span>
          <span class="text">{{ log.text }}</span>
        </div>
        <div class="log-line typing" v-if="isRunning">
          <span class="prefix">&gt;</span>
          <span class="cursor">_</span>
        </div>

        <div class="completion-banner" v-if="isCompleted">
          <div class="banner-title">⚡ MODEL ENSEMBLE RANKING COMPLETE ⚡</div>
          <div class="top-ranks">
            <span v-for="item in topRankings" :key="item.number" class="rank-chip">
              #{{ item.number }} (评分: {{ item.score }})
            </span>
          </div>
          <button class="view-btn" @click="closeTerminal">查看完整仪表盘盘面 ➔</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, nextTick } from 'vue'

const props = defineProps({
  visible: {
    type: Boolean,
    default: false
  },
  rankings: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['close'])

const logs = ref([])
const isRunning = ref(false)
const isCompleted = ref(false)
const terminalBody = ref(null)
const topRankings = ref([])

const steps = [
  { text: "INITIALIZING AI LOTTERY MATRIX KERNEL v1.0.0...", type: "sys", delay: 200 },
  { text: "CONNECTING TO DUAL DATA SOURCE: MacauJC API & KJ1868 API...", type: "info", delay: 300 },
  { text: "VERIFYING DATA INTEGRITY: Checking 500 draws for anomaly & checksums... [OK]", type: "success", delay: 350 },
  { text: "EXTRACTING FEATURE VECTOR: 196 dimensions (Missing, Frequency, Interval, Color)...", type: "info", delay: 350 },
  { text: "EXECUTING MODEL 1/6: Markov Chain (Order 1-3) Transition Probabilities...", type: "run", delay: 300 },
  { text: "EXECUTING MODEL 2/6: Bayesian Model Posterior Update & Evidence Weights...", type: "run", delay: 300 },
  { text: "EXECUTING MODEL 3/6: Random Forest Ensemble (50 Decision Trees Classification)...", type: "run", delay: 350 },
  { text: "EXECUTING MODEL 4/6: XGBoost Gradient Boosting Tree Inference...", type: "run", delay: 350 },
  { text: "EXECUTING MODEL 5/6: LightGBM Histogram Optimization & Probability Normalization...", type: "run", delay: 300 },
  { text: "EXECUTING MODEL 6/6: PyTorch LSTM Sequence Neural Network Tensor (Seq_Len=30)...", type: "run", delay: 400 },
  { text: "COMPUTING ENSEMBLE FUSION: Weighted Aggregation & Consensus Index Calculation...", type: "sys", delay: 300 },
  { text: "INFERENCE COMPLETE: Target next special number ranking locked.", type: "success", delay: 200 }
]

function getCurrentTime() {
  const now = new Date()
  return now.toTimeString().split(' ')[0] + '.' + String(now.getMilliseconds()).padStart(3, '0')
}

function scrollToBottom() {
  nextTick(() => {
    if (terminalBody.value) {
      terminalBody.value.scrollTop = terminalBody.value.scrollHeight
    }
  })
}

function runTerminalAnimation() {
  logs.value = []
  isRunning.value = true
  isCompleted.value = false
  topRankings.value = props.rankings.slice(0, 5)

  let stepIdx = 0

  function nextStep() {
    if (stepIdx < steps.length) {
      const step = steps[stepIdx]
      logs.value.push({
        time: getCurrentTime(),
        text: step.text,
        type: step.type
      })
      scrollToBottom()
      stepIdx++
      setTimeout(nextStep, step.delay)
    } else {
      isRunning.value = false
      isCompleted.value = true
      scrollToBottom()
    }
  }

  nextStep()
}

watch(() => props.visible, (newVal) => {
  if (newVal) {
    runTerminalAnimation()
  }
})

function closeTerminal() {
  emit('close')
}
</script>

<style scoped>
.hacker-terminal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.85);
  backdrop-filter: blur(6px);
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
}

.terminal-box {
  width: 880px;
  max-width: 92vw;
  height: 560px;
  background: #0d1117;
  border: 1px solid #30363d;
  border-radius: 10px;
  box-shadow: 0 0 30px rgba(0, 255, 100, 0.2);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  font-family: 'Fira Code', 'Courier New', Courier, monospace;
}

.terminal-header {
  background: #161b22;
  padding: 10px 16px;
  display: flex;
  align-items: center;
  border-bottom: 1px solid #30363d;
}

.window-buttons {
  display: flex;
  gap: 8px;
}

.dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
}

.dot.red { background: #ff5f56; }
.dot.yellow { background: #ffbd2e; }
.dot.green { background: #27c93f; }

.terminal-title {
  margin-left: 16px;
  font-size: 13px;
  color: #8b949e;
  font-weight: bold;
  letter-spacing: 1px;
}

.close-btn {
  margin-left: auto;
  background: transparent;
  border: none;
  color: #8b949e;
  font-size: 12px;
  cursor: pointer;
}
.close-btn:hover { color: #fff; }

.terminal-body {
  flex: 1;
  padding: 16px;
  overflow-y: auto;
  background: #090d12;
  color: #00ff66;
  position: relative;
}

.log-line {
  margin-bottom: 8px;
  font-size: 14px;
  line-height: 1.5;
  display: flex;
  gap: 8px;
}

.timestamp { color: #58a6ff; font-size: 12px; }
.prefix { color: #00ff66; font-weight: bold; }

.log-line.sys .text { color: #79c0ff; font-weight: bold; }
.log-line.info .text { color: #d2a8ff; }
.log-line.success .text { color: #56d364; font-weight: bold; }
.log-line.run .text { color: #ffa657; }

.cursor {
  animation: blink 0.8s infinite;
  color: #00ff66;
  font-weight: bold;
}

@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0; }
}

.completion-banner {
  margin-top: 20px;
  padding: 16px;
  background: rgba(0, 255, 102, 0.1);
  border: 1px solid #00ff66;
  border-radius: 6px;
  text-align: center;
  animation: fadeIn 0.5s ease-in-out;
}

.banner-title {
  font-size: 16px;
  font-weight: bold;
  color: #00ff66;
  margin-bottom: 12px;
  letter-spacing: 1px;
}

.top-ranks {
  display: flex;
  justify-content: center;
  gap: 12px;
  margin-bottom: 14px;
}

.rank-chip {
  background: #161b22;
  border: 1px solid #56d364;
  color: #fff;
  padding: 6px 12px;
  border-radius: 4px;
  font-size: 13px;
  font-weight: bold;
}

.view-btn {
  background: #238636;
  color: white;
  border: none;
  padding: 8px 18px;
  border-radius: 4px;
  font-weight: bold;
  cursor: pointer;
  font-size: 14px;
}
.view-btn:hover { background: #2ea043; }

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
