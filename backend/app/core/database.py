from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.domain.base_entity import BaseEntity


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
engine = create_async_engine(settings.DATABASE_URL, echo=True, future=True)

# Create session factory using the CustomAsyncSession class
async_session = sessionmaker(engine, class_=CustomAsyncSession, expire_on_commit=False)


# Dependency for FastAPI
async def get_db() -> AsyncSession:
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()
