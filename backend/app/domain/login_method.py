from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, UUID
from app.domain.base_entity import BaseEntity
import uuid

# Login Methods Table
class LoginMethod(BaseEntity):
    __tablename__ = 'login_methods'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    method_name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)  # e.g., 'email', 'google', 'github', 'facebook'
    description: Mapped[str] = mapped_column(Text, nullable=True)

    def __repr__(self) -> str:
        return f"LoginMethod(id={self.id}, method_name={self.method_name})"
