import mimetypes
import uuid

from fastapi import APIRouter, Depends, HTTPException, UploadFile, status, Form, requests
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from uuid import UUID

from core.dependencies import get_current_user
from core.infrastructure.database import get_db
from core.storage.document_storage_manager import DocumentStorageManager
from core.vectorstore.vector_store import VectorStore
from modules.document.application.document_service import DocumentService
from modules.document.infrastructure.document_repository import DocumentRepository
from modules.document.application.document_dto import (
    DocumentCreateRequest,
    DocumentUpdateRequest,
    DocumentResponse,
)

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
    dependencies=[Depends(get_current_user)]
)

storage_manager = DocumentStorageManager()  # Initialize storage manager

# ------------------------------------
# Dependency Injection
# ------------------------------------
def get_document_service(session: AsyncSession = Depends(get_db)) -> DocumentService:
    repository = DocumentRepository(session)
    return DocumentService(repository)

# async def store_file(file: UploadFile) -> str:
#     """Simulates storing a file and returns a storage URI."""
#     # Here you can integrate AWS S3, Azure Blob, or GCP Storage
#     file_id = str(uuid.uuid4())
#     storage_uri = f"s3://bucket/documents/{file_id}-{file.filename}"
#     print(f"File stored at: {storage_uri}")  # Simulating storage
#     return storage_uri

async def generate_embedding_uri(file_name: str) -> str:
    """Simulates generating an embedding URI for the document."""
    # Simulating vector database storage (e.g., ChromaDB, Pinecone)
    embedding_id = str(uuid.uuid4())
    embedding_uri = f"chroma://vectors/{embedding_id}-{file_name.replace(' ', '_')}"
    print(f"Embedding stored at: {embedding_uri}")  # Simulating embedding storage
    return embedding_uri


# ------------------------------------
# Routes
# ------------------------------------

vector_store = VectorStore()

@router.get("/health")
async def health_check():
    """Check if ChromaDB is running and authenticated."""
    response = requests.get(f"{vector_store.chroma_url}/api/v1/status", headers=vector_store.headers)
    if response.status_code == 200:
        return {"status": "ChromaDB is running and authenticated!"}
    else:
        raise HTTPException(status_code=500, detail="Failed to authenticate with ChromaDB")


@router.post("/upload", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(
        user_id: UUID = Form(...),
        title: Optional[str] = Form(None),
        description: Optional[str] = Form(None),
        tags: Optional[str] = Form(None),
        is_public: bool = Form(False),
        file: UploadFile = Form(...),
        service: DocumentService = Depends(get_document_service),
):
    """Uploads a document, extracts metadata, and creates a record."""

    # Store file in MinIO using DocumentStorageManager
    storage_uri = await storage_manager.store_file(file, str(user_id))

    # Generate embedding URI for vectorized content
    embedding_uri = await generate_embedding_uri(file.filename)

    # Create Document Request DTO
    create_request = DocumentCreateRequest(
        user_id=user_id,
        file_name=file.filename,
        file_type=file.content_type or "application/octet-stream",
        file_extension=file.filename.split(".")[-1].lower(),
        file_size=len(await file.read()),
        storage_uri=storage_uri,
        embedding_uri=embedding_uri,
        title=title,
        description=description,
        tags=tags,
        is_public=is_public,
    )

    # Call the Service Layer to Create the Document
    document_response = await service.create_document(create_request)

    return document_response

@router.post("/", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def create_document(
    request: DocumentCreateRequest,
    service: DocumentService = Depends(get_document_service),
):
    """Creates a new document."""
    return await service.create_document(request)


@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(
    document_id: UUID,
    service: DocumentService = Depends(get_document_service),
):
    """Gets a document by ID."""
    document = await service.get_document_by_id(document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return document


@router.patch("/{document_id}", response_model=DocumentResponse)
async def update_document(
    document_id: UUID,
    request: DocumentUpdateRequest,
    service: DocumentService = Depends(get_document_service),
):
    """Updates a document's metadata."""
    document = await service.update_document(document_id, request)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return document


@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(
    document_id: UUID,
    service: DocumentService = Depends(get_document_service),
):
    """Soft deletes a document."""
    await service.delete_document(document_id)
    return {"detail": "Document deleted"}


@router.post("/{document_id}/publish", status_code=status.HTTP_200_OK)
async def publish_document(
    document_id: UUID,
    service: DocumentService = Depends(get_document_service),
):
    """Publishes a document."""
    await service.publish_document(document_id)
    return {"detail": "Document published"}


@router.post("/{document_id}/archive", status_code=status.HTTP_200_OK)
async def archive_document(
    document_id: UUID,
    service: DocumentService = Depends(get_document_service),
):
    """Archives a document."""
    await service.archive_document(document_id)
    return {"detail": "Document archived"}
