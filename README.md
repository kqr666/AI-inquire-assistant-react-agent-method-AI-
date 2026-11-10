


🛠️ 技术栈

- **前端**：Vue 3 + TypeScript + Vite + Ant Design Vue + Axios + Vue Router
- **后端**：Python 3.10+ + FastAPI + Uvicorn + Pydantic
- **AI 与工具**：DeepSeek (大语言模型) + SerpAPI (谷歌网页搜索) + python-dotenv





## 📂 项目结构

```text
AI 查询代理/
├── backend/                 # 后端代码
│   ├── .env.example         # 环境变量模板（需重命名为 .env 并填入密钥）
│   ├── llm_client.py        # 大模型请求封装 (基于 OpenAI SDK)
│   ├── main.py              # FastAPI 主入口
│   ├── react_agent_demo.py  # ReAct 智能体核心循环逻辑
│   ├── tools.py             # 工具执行器与搜索工具定义
│   └── requirements.txt     # Python 依赖清单
│
├── frontend/                # 前端代码
│   ├── src/                 
│   │   ├── services/        # Axios API 请求封装
│   │   ├── types/           # TS 类型定义
│   │   ├── views/           # 页面组件 (Home.vue / Result.vue)
│   │   └── App.vue          # 根组件
│   ├── package.json         # Node 依赖清单
│   └── vite.config.ts       # Vite 配置
│
└── .gitignore               # Git 忽略清单

在运行后端之前，请确保 .env 文件中配置了以下变量：
# 大模型配置 (以 DeepSeek 为例)
LLM_MODEL_ID=deepseek-chat
LLM_API_KEY=sk-xxxxxxxxxxxxxxxxx
LLM_BASE_URL=https://api.deepseek.com
LLM_TIMEOUT=60

# 搜索引擎配置 (SerpAPI)
SERPAPI_API_KEY=xxxxxxxxxxxxxxxxx

启动后端（The Brain）
cd backend
Windows 系统：
.venv\Scripts\activate
Mac/Linux 系统：
source .venv/bin/activate

(激活成功后，终端最前面会出现绿色的 (.venv) 字样)

检查环境变量：确保 backend 目录下有一个 .env 文件，里面填好了你的两个 Key（不要带双引号）。
启动服务：
python main.py

启动前端（The Face）
cd frontend
安装依赖（只有第一次启动或者改了 package.json 时才需要跑）：
npm install
启动前端服务：
npm run dev


本项目基于helloagent开源，仅供学习与交流使用。
