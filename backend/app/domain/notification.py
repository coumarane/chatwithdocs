from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, TIMESTAMP, func, UUID, ForeignKey
from app.domain.base_entity import BaseEntity
import uuid

class Notification(BaseEntity):
    __tablename__ = 'notifications'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)  # Tied to specific user
    organization_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('organizations.id', ondelete='CASCADE'), nullable=True)  # Optional for team-wide notifications
    message: Mapped[str] = mapped_column(Text, nullable=False)  # Notification content
    type: Mapped[str] = mapped_column(String(50), nullable=False, default='info')  # Type of notification ('info', 'error', 'success', etc.)
    channel: Mapped[str] = mapped_column(String(50), nullable=True, default='in-app')  # Delivery channel ('in-app', 'email', etc.)
    action_url: Mapped[str] = mapped_column(Text, nullable=True)  # Optional URL for user actions
    priority: Mapped[str] = mapped_column(String(20), nullable=True, default='low')  # Notification priority ('low', 'medium', 'high')
    status: Mapped[str] = mapped_column(String(50), nullable=True, default='unread')  # Notification status ('unread', 'read')
    expires_at: Mapped[str] = mapped_column(TIMESTAMP, nullable=True)  # Expiry time for the notification

    def __repr__(self) -> str:
        return f"Notification(id={self.id}, user_id={self.user_id}, message={self.message}, type={self.type})"
