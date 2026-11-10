"""FastAPI主应用 - AI 查询代理"""

import os
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 导入核心组件 (请确保文件名与你本地的一致)
from llm_client import HelloAgentsLLM
from tools import ToolExecutor, search
# 假设你的主文件名叫 react_agency_demo.py，里面包含 ReActAgent 类
from react_ageny_demo import ReActAgent

# ==========================================
# 1. 创建 FastAPI 应用 (总公司挂牌)
# ==========================================
app = FastAPI(
    title="AI 智能查询代理",
    version="1.0.0",
    description="基于 ReAct 范式的智能搜索与问答助手 API",
    docs_url="/docs",
    redoc_url="/redoc"
)

# ==========================================
# 2. 配置 CORS 跨域保安
# ==========================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有前端跨域请求 (开发阶段)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# 3. 全局变量声明 (工位准备)
# ==========================================
agent = None  # 稍后在 startup 事件中真正雇佣


# ==========================================
# 4. 数据模型定义 (点菜单与上菜标准)
# ==========================================
class ChatRequest(BaseModel):
    question: str = Field(..., description="用户向 AI 提出的问题", example="帮我查一下苏州明天的天气")


class ChatResponse(BaseModel):
    success: bool = Field(..., description="是否成功获取答案")
    answer: str = Field(..., description="Agent 思考后的最终答案")


# ==========================================
# 5. 生命周期事件 (开业仪式与关门仪式)
# ==========================================
@app.on_event("startup")
async def startup_event():
    """应用启动事件"""
    global agent

    print("\n" + "=" * 60)
    print(f"🚀 AI 智能查询代理 v1.0.0")
    print("=" * 60)

    # 验证大模型配置是否齐全
    if not os.getenv("LLM_API_KEY"):
        print("❌ 配置验证失败: 未找到 LLM_API_KEY，请检查 .env 文件")
        raise ValueError("缺少核心配置")
    print("✅ 大模型配置验证通过")

    # 初始化智能体系统
    print("\n🔄 正在唤醒智能体...")
    try:
        llm = HelloAgentsLLM()
        tool_executor = ToolExecutor()

        # 注册武器
        search_desc = "一个网页搜索引擎。当你需要回答关于时事、事实以及在你的知识库中找不到的信息时，应使用此工具。"
        tool_executor.registerTool("Search", search_desc, search)

        # 雇佣包工头
        agent = ReActAgent(llm_client=llm, tool_executor=tool_executor)
        print("✅ 智能体系统初始化完成！")
    except Exception as e:
        print(f"❌ 智能体初始化失败: {e}")
        raise e

    print("\n" + "=" * 60)
    print("📚 API文档: http://localhost:8000/docs")
    print("📖 ReDoc文档: http://localhost:8000/redoc")
    print("=" * 60 + "\n")


@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭事件"""
    print("\n" + "=" * 60)
    print("👋 应用正在关闭...")
    print("=" * 60 + "\n")


# ==========================================
# 6. 业务与健康接口 (窗口接待)
# ==========================================
@app.get("/")
async def root():
    """根路径"""
    return {
        "name": "AI 智能查询代理",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }


@app.get("/health")
async def health():
    """健康检查"""
    return {
        "status": "healthy",
        "service": "react-agent-service",
        "version": "1.0.0"
    }


@app.post("/api/chat", response_model=ChatResponse)
def chat_with_agent(request: ChatRequest):
    """
    核心业务窗口：接收前端问题，阻塞等待 Agent 思考完毕，返回最终答案。
    (注意：这里故意用普通的 def，因为 agent.run 是同步阻塞的，FastAPI 会自动把它扔进线程池，不卡死主程序)
    """
    if agent is None:
        raise HTTPException(status_code=503, detail="系统正在初始化，请稍后再试")

    print(f"\n📥 收到前端提问: {request.question}")

    try:
        # 启动循环
        final_answer = agent.run(request.question)

        if final_answer:
            return ChatResponse(success=True, answer=final_answer)
        else:
            return ChatResponse(success=False, answer="抱歉，Agent 思考步数超限，未能找到最终答案。")

    except Exception as e:
        print(f"❌ 发生严重错误: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ==========================================
# 7. 启动入口 (点火开关)
# ==========================================
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )