from fastapi import APIRouter, Body
from app.agent.summary_agent import SummaryAgent
from app.agent.rewrite_agent import RewriteAgent
from app.agent.uml_agent import UmlAgent
from app.model.schema import AIRequest, SummaryResponse, RewriteResponse, UmlResponse

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
