import datetime
from typing import Optional
from sqlalchemy import DateTime, MetaData, func, String
from sqlalchemy.ext.asyncio import (
    AsyncAttrs
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class BaseEntity(AsyncAttrs, DeclarativeBase):
    """Base class for all models"""

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

    # Common timestamp fields
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    # Common user tracking fields
    user_created: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    user_updated: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    def update_metadata(self, current_user: Optional[str] = None):
        now = func.now()
        if not self.created_at:
            self.created_at = now
            self.user_created = current_user
        self.updated_at = now
        self.user_updated = current_user