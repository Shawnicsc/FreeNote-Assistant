from fastapi import APIRouter, Body, HTTPException
from app.agent.summary_agent import SummaryAgent
from app.agent.rewrite_agent import RewriteAgent
from app.agent.uml_agent import UmlAgent
from app.config import get_settings
from app.core.llm_factory import config_manager, get_llm
from app.model.schema import AIRequest, SummaryResponse, RewriteResponse, UmlResponse, RagRequest, ConfigUpdateRequest, \
    RAGResponse
from app.rag.chain import build_rag_chain
from app.rag.loader import load_markdown_docs
from app.rag.splitter import split_docs
from app.rag.vectorstore import build_vectorstore

router = APIRouter()
settings = get_settings()

docs = load_markdown_docs(settings.local_file_path)
chunks = split_docs(docs)
vectorstore = build_vectorstore(chunks)
rag_chain = build_rag_chain(get_llm(), vectorstore)

@router.post("/summary", response_model=SummaryResponse)
async def summary(request: AIRequest):
    """
    智能总结接口
    """
    agent = SummaryAgent()
    return agent.run(request.content)

@router.post("/rewrite", response_model=RewriteResponse)
async def rewrite(request: AIRequest):
    """
    智能润色接口
    """
    agent = RewriteAgent()
    return agent.run(request.content)

@router.post("/uml", response_model=UmlResponse)
async def generate_uml(request: AIRequest):
    """
    UML 图表生成接口 (Tool Call 方式)
    """
    agent = UmlAgent()
    return agent.run(request.content)
@router.post("/rag")
async def rag_answer(data: RagRequest) :
    """
     RAG回答
    """
    result = rag_chain(data.question)
    return {
        "answer": result["result"],
        "sources": [
            doc.metadata.get("source")
            for doc in result["source_documents"]
        ]
    }

@router.post("/config/update")
async def update_ai_config(request: ConfigUpdateRequest):
    """
    动态更新 AI 配置接口
    """
    config_manager.update_config(
        api_key=request.api_key,
        base_url=request.base_url,
        model_id=request.model_id
    )
    return {"status": "success", "message": "AI configuration updated"}

@router.get("/config")
async def get_ai_config():
    """
    获取当前 AI 配置
    """
    return {
        "api_key": config_manager.api_key[:8] + "******" if config_manager.api_key else None,
        "base_url": config_manager.base_url,
        "model_id": config_manager.model_id
    }
