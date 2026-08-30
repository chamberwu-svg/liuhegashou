# AI Lottery Prediction Lab (AI 预测实验室)

多模型概率分析与历史回测平台 (Multi-Model Probability Analysis Platform v1.0)

## 🌟 核心功能

- **数据源自动同步**：集成 MacauJC (`https://macaujc.com/api/history`) 与 KJ1868 (`https://www.kj1868.cc/api/drawHistory`) 开奖数据爬虫与 SQLite 本地缓存。
- **6 大独立 AI / ML 模型**：
  - **Markov**：1阶/2阶/3阶 状态转移概率。
  - **Bayesian**：先验分布 + 遗漏值/冷热动态更新后验概率。
  - **Random Forest**：高维结构化遗漏与频次特征分类打分。
  - **XGBoost**：高精度 GBDT 多分类预测。
  - **LightGBM**：高效直方图 GBDT 多分类预测。
  - **LSTM 神经网络**：基于 PyTorch 的多时序窗口 (20/30/50/100期) 深度学习预测。
- **模型融合与共识引擎**：
  - 动态统计 Top-10 预测结果中 6/6 模型支持度。
  - 按权重合成 01～49 综合得分排名。
- **Walk-Forward 自动回测系统**：
  - 逐期滚动回测计算 Top1 / Top5 / Top10 命中率及平均排名，与 1/49 (≈2.04%) 随机基准进行对照。
- **Vue 3 预测中心 Dashboard**：
  - 包含 Dashboard 预测中心、Training 模型训练控制台、Models 原理分析、Backtest 历史回测四大完整页面。

---

## 🚀 Docker 部署指南 (推荐)

项目已提供完整的生产级 Dockerfile 与 docker-compose 配置。

### 1. 一键启动 (Frontend + Backend + Nginx)

```bash
cd ai-lottery-lab
docker compose up -d --build
```

启动成功后：
- **前端 Web 界面**：`http://localhost` (端口 80)
- **后端 API 服务**：`http://localhost:8000` (端口 8000)
- **Swagger API 文档**：`http://localhost:8000/docs`

---

## 💻 本地开发环境运行

### 1. 启动后端 API

```bash
cd ai-lottery-lab
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 运行 FastAPI 服务
cd backend
PYTHONPATH=. uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 2. 启动前端 Vue 3 应用

```bash
cd ai-lottery-lab/frontend
npm install
npm run dev
```

访问 `http://localhost:3000` 即可启动开发界面。

---

## 🧪 单元测试

```bash
cd ai-lottery-lab/backend
PYTHONPATH=. ../.venv/bin/python -m pytest ../tests/test_model_core.py ../tests/test_api.py -v
```

---

## 🚂 Railway 云端一键部署指南

项目已提供针对 [Railway](https://railway.app) 部署的配置：
- `railway.toml`：声明部署健康检查路径 `/health` 与启动命令。
- `nixpacks.toml`：自动安装 GCC / libgomp 等 C++ 动态库依赖，保障 XGBoost / LightGBM 正常加载。
- `Dockerfile`：支持 Railway Docker 构建引擎。

### 部署步骤：

1. 登录 [Railway Console](https://railway.app) 并新建项目。
2. 选择 **"Deploy from GitHub repo"** 并选中本仓库。
3. Railway 会自动读取根目录下的 `railway.toml` / `nixpacks.toml` 或 `Dockerfile` 进行构建部署。
4. 部署完成后，在 Railway 设置中开启 **Public Networking Domain**，即可生成公共访问域名。

---

## ⚠️ 免责声明

本系统为数据分析与机器学习概率研究平台，所有预测结果均由模型基于历史开奖数据统计计算得出，**不构成任何投资或下注建议**。


