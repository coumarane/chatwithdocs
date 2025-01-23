from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, TIMESTAMP, func, UUID, Boolean
from sqlalchemy import CheckConstraint
from app.domain.base_entity import BaseEntity
import uuid

class User(BaseEntity):
    __tablename__ = 'users'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(Text, nullable=False)
    user_name: Mapped[str] = mapped_column(String(255), nullable=True)
    first_name: Mapped[str] = mapped_column(String(255), nullable=True)
    last_name: Mapped[str] = mapped_column(String(255), nullable=True)
    status: Mapped[str] = mapped_column(String(50), nullable=True, default='active')  # e.g., 'active', 'inactive', 'banned'
    is_email_verified: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)  # Tracks email verification status
    verification_token: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), default=uuid.uuid4)  # Token for email verification

    __table_args__ = (
        CheckConstraint('email ~* \'^[^@]+@[^@]+\\.[^@]+$\'', name='chk_email_format'),  # Basic email format validation
    )

    def __repr__(self) -> str:
        return f"User(id={self.id}, email={self.email}, user_name={self.user_name})"
