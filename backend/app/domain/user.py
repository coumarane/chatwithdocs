from datetime import datetime
# from sqlalchemy import Column, Integer, String
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column
from app.domain.base_entity import BaseEntity

class User(BaseEntity):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    date_of_birth: Mapped[str] = mapped_column(nullable=True)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )
    deleted_at: Mapped[datetime | None]

    def __repr__(self) -> str:
        return f"users(id={self.id})"
