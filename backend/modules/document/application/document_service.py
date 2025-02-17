from typing import List, Optional
from uuid import UUID
from modules.document.domain.document import Document
from modules.document.infrastructure.document_repository import DocumentRepository
from modules.document.application.document_dto import (
    DocumentCreateRequest,
    DocumentUpdateRequest,
    DocumentResponse,
)

class DocumentService:
    """Application Service: Contains use case logic for Documents."""

    def __init__(self, repository: DocumentRepository):
        self.repository = repository

    async def create_document(self, request: DocumentCreateRequest) -> DocumentResponse:
        """Creates a new document."""

        # Check if user is valid and has permission

        document = Document(
            user_id=request.user_id,
            file_name=request.file_name,
            file_type=request.file_type,
            file_extension=request.file_extension,
            file_size=request.file_size,
            storage_uri=request.storage_uri,
            embedding_uri=request.embedding_uri,
            title=request.title,
            description=request.description,
            tags=request.tags,
            is_public=request.is_public,
        )
        await self.repository.save(document)
        return DocumentResponse.from_domain(document)

    async def get_document_by_id(self, document_id: UUID) -> Optional[DocumentResponse]:
        """Retrieves a document by its ID."""
        document = await self.repository.get_by_id(str(document_id))
        if document:
            return DocumentResponse.from_domain(document)
        return None

    async def update_document(self, document_id: UUID, request: DocumentUpdateRequest) -> Optional[DocumentResponse]:
        """Updates document metadata."""
        fields_to_update = {k: v for k, v in request.dict().items() if v is not None}
        if fields_to_update:
            await self.repository.update_fields(str(document_id), fields_to_update)
        document = await self.repository.get_by_id(str(document_id))
        return DocumentResponse.from_domain(document) if document else None

    async def delete_document(self, document_id: UUID) -> bool:
        """Soft deletes a document."""
        await self.repository.delete(str(document_id))
        return True

    async def publish_document(self, document_id: UUID) -> bool:
        """Publishes a document."""
        await self.repository.publish(str(document_id))
        return True

    async def archive_document(self, document_id: UUID) -> bool:
        """Archives a document."""
        await self.repository.archive(str(document_id))
        return True
