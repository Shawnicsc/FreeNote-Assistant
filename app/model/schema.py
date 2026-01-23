from datetime import datetime, timezone

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



