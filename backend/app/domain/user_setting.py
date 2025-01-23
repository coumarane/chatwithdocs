from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, TIMESTAMP, UUID, ForeignKey, func
from sqlalchemy import JSON, UniqueConstraint
from app.domain.base_entity import BaseEntity
import uuid

class UserSetting(BaseEntity):
    __tablename__ = 'user_settings'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    setting_key: Mapped[str] = mapped_column(String(255), nullable=False)  # Key for the setting (e.g., 'theme', 'notifications')
    setting_value: Mapped[dict] = mapped_column(JSON, nullable=False)  # Value of the setting, stored as JSON
    updated_at: Mapped[str] = mapped_column(TIMESTAMP, server_default=func.now(), nullable=False)

    __table_args__ = (
        UniqueConstraint('user_id', 'setting_key', name='unique_user_setting'),  # Ensures unique settings per user
    )

    def __repr__(self) -> str:
        return f"UserSetting(id={self.id}, user_id={self.user_id}, setting_key={self.setting_key}, setting_value={self.setting_value})"
