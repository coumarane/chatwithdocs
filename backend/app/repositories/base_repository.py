import uuid

from sqlalchemy import delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from typing import Type, TypeVar, List, Optional
from app.domain import BaseEntity

T = TypeVar("T")  # Declare a type variable for the models

class BaseRepository:
    def __init__(self, db_session: AsyncSession):
        """
        Initializes the BaseRepository with an AsyncSession.

        :param db_session: The async database session to be used.
        """
        self.db_session = db_session

    async def get(self, model: Type[T], id: str) -> Optional[T]:
        """Get a single object by id."""
        async with self.db_session as session:
            result = await session.execute(select(model).filter(model.id == id))
            return result.scalar_one_or_none()

    async def get_all(self, model: Type[T]) -> List[T]:
        """Get all objects of a specific model."""
        async with self.db_session as session:
            result = await session.execute(select(model))
            return result.scalars().all()

    async def create(self, model: Type[T], data: dict) -> T:
        """Create a new object in the database."""
        async with self.db_session as session:
            obj = model(**data)
            session.add(obj)
            await session.commit()
            await session.refresh(obj)  # Refresh the object to get the latest data from DB
            return obj

    async def update(self, model: Type[T], id: str, data: dict) -> Optional[T]:
        """Update an existing object by id."""
        async with self.db_session as session:
            stmt = update(model).where(model.id == id).values(**data).returning(model)
            result = await session.execute(stmt)
            updated_obj = result.scalar_one_or_none()
            await session.commit()
            return updated_obj

    async def delete(self, model: Type[T], id: str) -> bool:
        """Delete an object by id."""
        async with self.db_session as session:
            stmt = delete(model).where(model.id == id)
            result = await session.execute(stmt)
            await session.commit()
            return result.rowcount > 0

    async def get_by_filter(self, model: Type[T], **filters) -> List[T]:
        """Get objects by applying filters."""
        async with self.db_session as session:
            stmt = select(model).filter_by(**filters)
            result = await session.execute(stmt)
            return result.scalars().all()

    async def get_paginated(self, model: Type[T], page: int = 1, page_size: int = 10) -> List[T]:
        """Get a paginated list of objects."""
        offset = (page - 1) * page_size  # Calculate offset based on page and page size
        async with self.db_session as session:
            stmt = select(model).offset(offset).limit(page_size)
            result = await session.execute(stmt)
            return result.scalars().all()