import datetime
import uuid
from typing import Optional
from sqlalchemy import DateTime, String, func, MetaData
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs

class BaseEntity(AsyncAttrs, DeclarativeBase):
    """Base class for all SQLAlchemy models (Persistence Layer)."""

    metadata = MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_`%(constraint_name)s`",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        }
    )

    type_annotation_map = {
        datetime.datetime: DateTime(timezone=True),
    }

    id: Mapped[uuid.UUID] = mapped_column(
        default=uuid.uuid4, primary_key=True
    )
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )
    user_created: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    user_updated: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    def update_metadata(self, current_user: Optional[str] = None):
        """Updates metadata fields."""
        self.updated_at = func.now()
        self.user_updated = current_user
