from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, TIMESTAMP, UUID, ForeignKey, func
from sqlalchemy import UniqueConstraint
from app.domain.base_entity import BaseEntity
import uuid

# User Social Logins Table
class UserSocialLogin(BaseEntity):
    __tablename__ = 'user_social_logins'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    login_method_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('login_methods.id', ondelete='CASCADE'), nullable=False)
    provider_user_id: Mapped[str] = mapped_column(String(255), nullable=False)  # ID provided by the social network
    access_token: Mapped[str] = mapped_column(Text, nullable=True)  # (Optional) For storing encrypted access tokens
    refresh_token: Mapped[str] = mapped_column(Text, nullable=True)  # (Optional) For storing encrypted refresh tokens
    expires_at: Mapped[str] = mapped_column(TIMESTAMP, nullable=True)  # (Optional) Token expiration time
    linked_at: Mapped[str] = mapped_column(TIMESTAMP, server_default=func.now(), nullable=False)

    __table_args__ = (
        UniqueConstraint('login_method_id', 'provider_user_id', name='unique_provider_user_id'),  # Ensure uniqueness for provider-user combos
    )

    def __repr__(self) -> str:
        return f"UserSocialLogin(id={self.id}, user_id={self.user_id}, login_method_id={self.login_method_id}, provider_user_id={self.provider_user_id})"
