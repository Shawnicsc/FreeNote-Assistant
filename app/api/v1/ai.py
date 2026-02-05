from fastapi import APIRouter, Body, HTTPException
from app.agent.summary_agent import SummaryAgent
from app.agent.rewrite_agent import RewriteAgent
from app.agent.uml_agent import UmlAgent
from app.service.rag_service import rag_service
from app.core.llm_factory import config_manager
from app.model.schema import AIRequest, SummaryResponse, RewriteResponse, UmlResponse, RagRequest, ConfigUpdateRequest

router = APIRouter()

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
async def rag_query(request: RagRequest):
    """
    RAG 知识库问答接口
    """
    try:
        answer = rag_service.query(request.question)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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
