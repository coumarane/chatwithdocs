import uuid

from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Boolean, Text, Enum
from sqlalchemy.dialects.postgresql import UUID
from core.infrastructure.base_entity import BaseEntity
from modules.document.domain.document import Document
from modules.document.domain.document_status import DocumentStatus
from modules.document.domain.lifecycle_status import LifecycleStatus


class DocumentORM(BaseEntity):
    """SQLAlchemy ORM model for Document (Persistence Layer)."""

    __tablename__ = "documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    file_name = Column(String(255), nullable=False)
    file_type = Column(String(100), nullable=False)
    file_extension = Column(String(20), nullable=False)
    file_size = Column(Integer, nullable=False)
    checksum = Column(String(128), nullable=True)

    storage_uri = Column(String(500), nullable=False)
    embedding_uri = Column(String(500), nullable=True)

    title = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    tags = Column(Text, nullable=True)

    document_status = Column(Enum(DocumentStatus), nullable=False, default=DocumentStatus.UPLOADED)
    lifecycle_status = Column(Enum(LifecycleStatus), nullable=False, default=LifecycleStatus.DRAFT)

    is_public = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=False)

    @staticmethod
    def from_domain(document: Document) -> "DocumentORM":
        """Converts Domain Document object to ORM object."""
        return DocumentORM(
            id=document.id,
            user_id=document.user_id,
            file_name=document.file_name,
            file_type=document.file_type,
            file_extension=document.file_extension,
            file_size=document.file_size,
            checksum=document.checksum,
            storage_uri=document.storage_uri,
            embedding_uri=document.embedding_uri,
            title=document.title,
            description=document.description,
            tags=document.tags,
            document_status=document.document_status,
            lifecycle_status=document.lifecycle_status,
            is_public=document.is_public,
            is_deleted=document.is_deleted,
            created_at=document.created_at,
            updated_at=document.updated_at,
            user_created=document.user_created,
            user_updated=document.user_updated,
        )

    def to_domain(self):
        """Converts ORM object to Domain Document object."""
        return Document(
            id=self.id,
            user_id=self.user_id,
            file_name=self.file_name,
            file_type=self.file_type,
            file_extension=self.file_extension,
            file_size=self.file_size,
            checksum=self.checksum,
            storage_uri=self.storage_uri,
            embedding_uri=self.embedding_uri,
            title=self.title,
            description=self.description,
            tags=self.tags,
            document_status=self.document_status,
            lifecycle_status=self.lifecycle_status,
            is_public=self.is_public,
            is_deleted=self.is_deleted,
            created_at=self.created_at,
            updated_at=self.updated_at,
            user_created=self.user_created,
            user_updated=self.user_updated,
        )
