from fastapi import APIRouter
from app.tools.document_tool import read_document
from app.model.schema import Document

router = APIRouter()

@router.get("/", response_model=list[Document])
async def get_docs():
    """
    获取所有本地文档
    """
    return read_document()

@router.get("/health")
async def health():
    """
    健康检查
    """
    return {"status": "ok"}
