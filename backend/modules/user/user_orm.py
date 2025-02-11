import uuid
from sqlalchemy import Column, String, Boolean, Text, Enum, UUID
from sqlalchemy.orm import Mapped, mapped_column
from core.infrastructure.base_entity import BaseEntity# Import domain enum
from modules.user.user import User
from modules.user.user_status_enum import UserStatusEnum


class UserORM(BaseEntity):
    """Database model for User, using SQLAlchemy (Persistence Layer)."""

    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(Text, nullable=False)
    user_name: Mapped[str] = mapped_column(String(255), nullable=True)
    first_name: Mapped[str] = mapped_column(String(255), nullable=True)
    last_name: Mapped[str] = mapped_column(String(255), nullable=True)
    status: Mapped[UserStatusEnum] = mapped_column(Enum(UserStatusEnum), nullable=False, default=UserStatusEnum.ACTIVE)
    is_email_verified: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    verification_token: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), default=uuid.uuid4)
    has_agreed_terms: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    @staticmethod
    def from_domain(user: User) -> "UserORM":
        """Converts a domain User object to an ORM UserORM object."""
        return UserORM(
            id=user.id,
            email=user.email,
            hashed_password=user.hashed_password,
            user_name=user.user_name,
            first_name=user.first_name,
            last_name=user.last_name,
            status=user.status,
            is_email_verified=user.is_email_verified,
            verification_token=user.verification_token,
            has_agreed_terms=user.has_agreed_terms,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )

    def to_domain(self) -> User:
        """Converts an ORM UserORM object back to a domain User object."""
        return User(
            id=self.id,
            email=self.email,
            hashed_password=self.hashed_password,
            user_name=self.user_name,
            first_name=self.first_name,
            last_name=self.last_name,
            status=self.status,
            is_email_verified=self.is_email_verified,
            verification_token=self.verification_token,
            has_agreed_terms=self.has_agreed_terms,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

