from typing import Optional, AsyncGenerator, Generator
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, Session
from app.domain.base_entity import BaseEntity
from core.config.config import settings

# =========================
# ASYNC ENGINE (FastAPI)
# =========================

# Custom AsyncSession
class CustomAsyncSession(AsyncSession):
    async def commit(self, current_user: Optional[str] = None):
        # Update metadata for all new or dirty entities
        for obj in self.new | self.dirty:
            if isinstance(obj, BaseEntity):
                obj.update_metadata(current_user)
        # Proceed with the commit
        await super().commit()


# Create the async engine
async_engine = create_async_engine(settings.DATABASE_URL, echo=True, future=True)

# Create session factory using the CustomAsyncSession class
async_session = sessionmaker(
    async_engine,
    class_=CustomAsyncSession,
    expire_on_commit=False
)


# Dependency for FastAPI
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()


# =========================
# SYNC ENGINE (Celery)
# =========================
class CustomSyncSession(Session):
    def commit(self, current_user: Optional[str] = None):
        # Update metadata for all new or dirty entities
        for obj in self.new | self.dirty:
            if isinstance(obj, BaseEntity):
                obj.update_metadata(current_user)
        super().commit()


# Convert async URL to sync-friendly
SYNC_DATABASE_URL = settings.DATABASE_URL.replace("postgresql+asyncpg", "postgresql")

# Sync Engine & Session
sync_engine = create_engine(SYNC_DATABASE_URL, echo=True, future=True)

SessionLocal = sessionmaker(
    bind=sync_engine,
    class_=CustomSyncSession,
    expire_on_commit=False
)

# Dependency for Celery (manual use)
def get_sync_db() -> Generator[Session, None, None]:
    with SessionLocal() as session:
        try:
            yield session
        finally:
            session.close()