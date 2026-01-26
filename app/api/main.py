# 获取配置
from fastapi import FastAPI

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


@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}


@app.get("/get_docs")
def get_docs():
    documents = read_document()
    return  documents


@app.get("/summary")
def summary():
    documents = read_document()
    summary_agent = SummaryAgent()
    result = []

    for doc in documents:
        res = summary_agent.run(document_content=doc.document_content)
        result.append(res)

    return result

@app.get("/rewrite")
def rewrite():
    documents = read_document()
    rewrite_agent = RewriteAgent()
    result = []

    for doc in documents:
        if doc.document_title == "AI 大模型应用开发笔记":
            result.append(rewrite_agent.run(doc.document_content))

    return result