# 获取配置
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.api import api_router
from app.config import get_settings

settings = get_settings()

# 创建 FastAPI 应用
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
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册 API 路由
app.include_router(api_router, prefix="/api/v1")

# 为了向后兼容，保留根路径健康检查
@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}