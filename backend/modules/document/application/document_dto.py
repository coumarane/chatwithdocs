from pydantic import BaseModel, UUID4
from typing import Optional

from modules.document.domain.document_status import DocumentStatus
from modules.document.domain.lifecycle_status import LifecycleStatus


# ------------------------------------
# Request DTOs
# ------------------------------------

class DocumentCreateRequest(BaseModel):
    user_id: UUID4
    file_name: str
    file_type: str
    file_extension: str
    file_size: int
    storage_uri: str
    embedding_uri: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[str] = None
    is_public: bool = False


class DocumentUpdateRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[str] = None


# ------------------------------------
# Response DTOs
# ------------------------------------

class DocumentResponse(BaseModel):
    id: UUID4
    user_id: UUID4
    file_name: str
    file_type: str
    file_size: int
    storage_uri: str
    embedding_uri: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[str] = None
    document_status: DocumentStatus
    lifecycle_status: LifecycleStatus
    is_public: bool
    is_deleted: bool
    created_at: str
    updated_at: str

    @classmethod
    def from_domain(cls, document):
        """Convert Domain Document to Response DTO."""
        return cls(
            id=document.id,
            user_id=document.user_id,
            file_name=document.file_name,
            file_type=document.file_type,
            file_size=document.file_size,
            storage_uri=document.storage_uri,
            embedding_uri=document.embedding_uri,
            title=document.title,
            description=document.description,
            tags=document.tags,
            document_status=document.document_status,
            lifecycle_status=document.lifecycle_status,
            is_public=document.is_public,
            is_deleted=document.is_deleted,
            created_at=document.created_at.isoformat(),
            updated_at=document.updated_at.isoformat(),
        )
