from datetime import datetime, timezone
from typing import Any, Optional

from pydantic import Field
from pydantic import BaseModel

def now():
    return datetime.now(timezone.utc)


class Document(BaseModel):
    document_id: str = Field(..., description="The unique identifier of the document")
    document_title: str = Field(..., description="The title of the document")
    document_content: str = Field(..., description="The content of the document")
    created_at: datetime = Field(default_factory=now)


class DocumentRequest(BaseModel):
    document_title: str = Field(..., description="The title of the document")
    document_content: str = Field(..., description="The content of the document")

class AIRequest(BaseModel):
    content: str

class RagRequest(BaseModel):
    question: str

class ConfigUpdateRequest(BaseModel):
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    model_id: Optional[str] = None

class SummaryStructure(BaseModel):
    section: str = Field(..., description="章节或主题名称")
    description: str = Field(..., description="该部分主要内容概述")

class SummaryResponse(BaseModel):
    title: str = Field(..., description="文档主题概括")
    summary: str = Field(..., description="全文总结")
    key_points: list[str] = Field(..., description="关键要点列表")
    structure: list[SummaryStructure] = Field(..., description="章节结构列表")

class RewriteResponse(BaseModel):
    title: str = Field(..., description="润色后的文档标题")
    rewritten_content: str = Field(..., description="完整润色后的文档正文")
    changes_summary: list[str] = Field(..., description="修改要点列表")

class UmlResponse(BaseModel):
    uml_code: str = Field(..., description="生成的 Mermaid UML 代码")
    uml_type: str = Field(..., description="UML 图表类型")
    description: str = Field(..., description="图表内容的简要描述")

class UmlEntity(BaseModel):
    id: str = Field(..., description="唯一标识符")
    label: str = Field(..., description="显示名称")
    type: str | None = Field(None, description="实体类型")

class UmlRelationship(BaseModel):
    source: str = Field(..., description="源实体 ID")
    target: str = Field(..., description="目标实体 ID")
    label: str | None = Field(None, description="关系描述")
    type: str | None = Field(None, description="关系类型")

class UmlIR(BaseModel):
    chart_type: str = Field(..., description="建议的图表类型")
    title: str = Field(..., description="图表标题")
    entities: list[UmlEntity] = Field(..., description="实体/节点列表")
    relationships: list[UmlRelationship] = Field(..., description="关系/连线列表")
    metadata: dict[str, Any] | None = Field(None, description="额外元数据")

class RAGRequest(BaseModel):
    question: str = Field(..., description="用户提出的问题")

class RAGResponse(BaseModel):
    answer: str = Field(..., description="基于检索内容生成的回答")
    source: list[str] = Field(..., description="用于回答的文档来源列表")

_next_id = 1

def create_document(document_request : DocumentRequest) -> Document:
    global _next_id

    document = Document(
        document_id=str(_next_id),
        document_title=document_request.document_title,
        document_content=document_request.document_content,
    )
    _next_id += 1
    return document



