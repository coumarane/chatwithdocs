from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update
from core.infrastructure.base_repository import BaseRepository
from modules.document.domain.lifecycle_status import LifecycleStatus
from modules.document.infrastructure.document_orm import DocumentORM
from modules.document.domain.document import Document

class DocumentRepository(BaseRepository):
    """Repository for Document entity."""

    def __init__(self, db: AsyncSession):
        super().__init__(db)  # Initialize BaseRepository with db session

    async def save(self, document: Document):
        """Saves or updates a Document."""
        document_orm = DocumentORM.from_domain(document)
        await self.db_session.merge(document_orm)
        await self.db_session.commit()

    async def get_by_id(self, document_id: str) -> Document | None:
        """Fetches a Document by ID."""
        result = await self.db_session.execute(select(DocumentORM).filter_by(id=document_id))
        document_orm = result.scalars().first()
        return document_orm.to_domain() if document_orm else None

    async def update_fields(self, document_id: str, fields: dict):
        """Updates specific fields of a Document."""
        stmt = (
            update(DocumentORM)
            .where(DocumentORM.id == document_id)
            .values(**fields)
        )
        await self.db_session.execute(stmt)
        await self.db_session.commit()

    async def delete(self, document_id: str):
        """Soft deletes a Document."""
        await self.update_fields(document_id, {"is_deleted": True})

    async def publish(self, document_id: str):
        """Publishes a Document."""
        await self.update_fields(document_id, {"lifecycle_status": LifecycleStatus.PUBLISHED})

    async def archive(self, document_id: str):
        """Archives a Document."""
        await self.update_fields(document_id, {"lifecycle_status": LifecycleStatus.ARCHIVED})
