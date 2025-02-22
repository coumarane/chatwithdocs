# from sqlalchemy import String, JSON, Enum, UUID
# from sqlalchemy.orm import Mapped, mapped_column
# from uuid import uuid4
# import enum
# from app.domain import BaseEntity
#
#
# class MessageStatusEnum(enum.Enum):
#     PENDING = "PENDING"
#     SENT = "SENT"
#     FAILED = "FAILED"
#
# class OutboxMessage(BaseEntity):
#     __tablename__ = 'outbox_message'
#
#     id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
#     event_type: Mapped[str] = mapped_column(String(255), nullable=False)  # e.g., "USER_REGISTERED", "PASSWORD_RESET"
#     payload: Mapped[dict] = mapped_column(JSON, nullable=False)  # Store event data in JSON format
#     status: Mapped[str] = mapped_column(Enum(MessageStatusEnum), default=MessageStatusEnum.PENDING)  # PENDING, SENT, FAILED
#
#     def __repr__(self) -> str:
#         return f"<OutboxMessage(id={self.id}, event_type={self.event_type}, status={self.status}, created_at={self.created_at})>"
#
