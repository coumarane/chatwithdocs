from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, UUID, TIMESTAMP, Boolean, ForeignKey, JSON, func, BigInteger
from app.domain.base_entity import BaseEntity
import uuid

# Organization or Team Management Table
class Organization(BaseEntity):
    __tablename__ = 'organizations'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    owner_user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    storage_limit: Mapped[int] = mapped_column(BigInteger, nullable=False, default=1073741824)  # Storage limit in bytes
    custom_branding: Mapped[dict] = mapped_column(JSON, nullable=True, default=None)  # Organization-specific settings
    created_at: Mapped[str] = mapped_column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at: Mapped[str] = mapped_column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)

    def __repr__(self) -> str:
        return f"Organization(id={self.id}, name={self.name}, owner_user_id={self.owner_user_id})"


# Organization Members Table
class OrganizationMember(BaseEntity):
    __tablename__ = 'organization_members'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('organizations.id', ondelete='CASCADE'), nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    role: Mapped[str] = mapped_column(String(50), nullable=False, default='member')  # 'admin', 'member'
    notifications_enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)  # User-specific settings
    joined_at: Mapped[str] = mapped_column(TIMESTAMP, server_default=func.now(), nullable=False)

    def __repr__(self) -> str:
        return f"OrganizationMember(id={self.id}, organization_id={self.organization_id}, user_id={self.user_id}, role={self.role})"


# Invitations Table
class Invitation(BaseEntity):
    __tablename__ = 'invitations'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('organizations.id', ondelete='CASCADE'), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    invited_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default='pending')  # 'pending', 'accepted', 'declined'
    created_at: Mapped[str] = mapped_column(TIMESTAMP, server_default=func.now(), nullable=False)

    def __repr__(self) -> str:
        return f"Invitation(id={self.id}, organization_id={self.organization_id}, email={self.email}, status={self.status})"
