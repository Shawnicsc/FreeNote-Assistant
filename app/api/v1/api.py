from fastapi import APIRouter
from app.api.v1.endpoints import ai, docs

api_router = APIRouter()

# 包含不同模块的路由
api_router.include_router(docs.router, prefix="/docs", tags=["Documents"])
api_router.include_router(ai.router, prefix="/ai", tags=["AI Assistant"])
