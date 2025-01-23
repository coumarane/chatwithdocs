from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, UUID
from app.domain.base_entity import BaseEntity
import uuid

# Features Table
class Feature(BaseEntity):
    __tablename__ = 'features'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)

    def __repr__(self) -> str:
        return f"Feature(id={self.id}, name={self.name})"