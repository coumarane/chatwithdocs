from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, TIMESTAMP, func, UUID, ForeignKey
from app.domain.base_entity import BaseEntity
import uuid

# Roles Table
class Role(BaseEntity):
    __tablename__ = 'roles'

    role_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    role_name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)

    def __repr__(self) -> str:
        return f"Role(role_id={self.role_id}, role_name={self.role_name})"


# User Roles Table
class UserRole(BaseEntity):
    __tablename__ = 'user_roles'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    role_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('roles.role_id', ondelete='CASCADE'), nullable=False)
    assigned_at: Mapped[str] = mapped_column(TIMESTAMP, server_default=func.now(), nullable=False)

    def __repr__(self) -> str:
        return f"UserRole(id={self.id}, user_id={self.user_id}, role_id={self.role_id})"


# Permissions Table
class Permission(BaseEntity):
    __tablename__ = 'permissions'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    permission_name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)

    def __repr__(self) -> str:
        return f"Permission(id={self.id}, permission_name={self.permission_name})"


# Role Permissions Table
class RolePermission(BaseEntity):
    __tablename__ = 'role_permissions'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    role_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('roles.role_id', ondelete='CASCADE'), nullable=False)
    permission_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('permissions.id', ondelete='CASCADE'), nullable=False)
    assigned_at: Mapped[str] = mapped_column(TIMESTAMP, server_default=func.now(), nullable=False)

    def __repr__(self) -> str:
        return f"RolePermission(id={self.id}, role_id={self.role_id}, permission_id={self.permission_id})"