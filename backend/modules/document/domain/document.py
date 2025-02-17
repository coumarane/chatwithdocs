import uuid
from datetime import datetime

from core.domain.domain_base import BaseDomain
from modules.document.domain.document_status import DocumentStatus
from modules.document.domain.lifecycle_status import LifecycleStatus


class Document(BaseDomain):
    """Domain Model: Represents a Document uploaded by a user."""

    def __init__(
            self,
            user_id: uuid.UUID,
            file_name: str,
            file_type: str,
            file_extension: str,
            file_size: int,
            storage_uri: str,
            embedding_uri: str = None,
            title: str = None,
            description: str = None,
            tags: str = None,
            document_status: DocumentStatus = DocumentStatus.UPLOADED,
            lifecycle_status: LifecycleStatus = LifecycleStatus.DRAFT,
            is_public: bool = False,
            is_deleted: bool = False,
            id: uuid.UUID = None,
            checksum: str = None,
            **kwargs,  # Allows metadata fields (created_at, updated_at, etc.)
    ):
        super().__init__(**kwargs)  # Initialize metadata fields

        self.id = id or uuid.uuid4()
        self.user_id = user_id
        self.file_name = file_name
        self.file_type = file_type
        self.file_extension = file_extension
        self.file_size = file_size
        self.checksum = checksum
        self.storage_uri = storage_uri
        self.embedding_uri = embedding_uri
        self.title = title
        self.description = description
        self.tags = tags
        self.document_status = document_status
        self.lifecycle_status = lifecycle_status
        self.is_public = is_public
        self.is_deleted = is_deleted

    def mark_as_deleted(self):
        """Soft delete the document."""
        self.is_deleted = True
        self.updated_at = datetime.utcnow()

    def publish(self):
        """Publish the document (change lifecycle status)."""
        self.lifecycle_status = LifecycleStatus.PUBLISHED
        self.updated_at = datetime.utcnow()

    def archive(self):
        """Archive the document."""
        self.lifecycle_status = LifecycleStatus.ARCHIVED
        self.updated_at = datetime.utcnow()

    def update_metadata(self, title: str = None, description: str = None, tags: str = None):
        """Update document metadata."""
        if title is not None:
            self.title = title
        if description is not None:
            self.description = description
        if tags is not None:
            self.tags = tags
        self.updated_at = datetime.utcnow()

    def __repr__(self):
        return (
            f"<Document(id={self.id}, file_name='{self.file_name}', "
            f"file_type='{self.file_type}', user_id={self.user_id}, "
            f"document_status='{self.document_status}', "
            f"lifecycle_status='{self.lifecycle_status}', created_at={self.created_at})>"
        )

