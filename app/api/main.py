# 获取配置
from fastapi import FastAPI

from app.config import get_settings

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