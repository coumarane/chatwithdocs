import uuid
from sqlalchemy import String, JSON, Enum, UUID
from sqlalchemy.orm import Mapped, mapped_column
from core.infrastructure.base_entity import BaseEntity
from modules.outbox_message.message_status_enum import MessageStatusEnum
from modules.outbox_message.outbox_message import OutboxMessage


class OutboxMessageORM(BaseEntity):
    """ORM model for Outbox messages (Persistence Layer)."""
    __tablename__ = 'outbox_message'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_type: Mapped[str] = mapped_column(String(255), nullable=False)
    payload: Mapped[dict] = mapped_column(JSON, nullable=False)
    status: Mapped[MessageStatusEnum] = mapped_column(Enum(MessageStatusEnum), default=MessageStatusEnum.PENDING)

    @staticmethod
    def from_domain(outbox_message) -> "OutboxMessageORM":
        """Converts a domain OutboxMessage object to an ORM object."""
        return OutboxMessageORM(
            id=outbox_message.id,
            event_type=outbox_message.event_type,
            payload=outbox_message.payload,
            status=outbox_message.status,
            created_at=outbox_message.created_at,
            updated_at=outbox_message.updated_at,
        )

    def to_domain(self):
        """Converts this ORM object back to a domain OutboxMessage object."""
        return OutboxMessage(
            event_type=self.event_type,
            payload=self.payload,
            status=self.status,
            id=self.id,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
