# 获取配置
from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.agent.rewrite_agent import RewriteAgent
from app.agent.summary_agent import SummaryAgent
from app.config import get_settings
from app.tools.document_tool import read_document

settings = get_settings()

# 创建FastAPI应用
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Free Note with AI Assistant",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有源，开发环境下建议
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法 (GET, POST, OPTIONS 等)
    allow_headers=["*"],  # 允许所有头
)

class AIRequest(BaseModel):
    content: str

@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}


@app.get("/get_docs")
def get_docs():
    documents = read_document()
    return  documents


@app.post("/summary")
def summary(request: AIRequest):
    summary_agent = SummaryAgent()
    res = summary_agent.run(document_content=request.content)
    return res

@app.post("/rewrite")
def rewrite(request: AIRequest):
    rewrite_agent = RewriteAgent()
    res = rewrite_agent.run(request.content)
    return res