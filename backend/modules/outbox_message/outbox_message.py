import uuid
import datetime
from typing import Dict
from modules.outbox_message.message_status_enum import MessageStatusEnum
from core.domain.domain_base import BaseDomain

class OutboxMessage(BaseDomain):
    """Domain Model for an Outbox Message (DDD - ORM Independent)."""

    def __init__(
        self,
        event_type: str,
        payload: Dict,
        status: MessageStatusEnum = MessageStatusEnum.PENDING,
        id: uuid.UUID = None,
        created_at: datetime.datetime = None,
        updated_at: datetime.datetime = None,
    ):
        super().__init__(id=id, created_at=created_at, updated_at=updated_at)
        self.event_type = event_type
        self.payload = payload
        self.status = status

    def mark_as_sent(self):
        """Marks the message as SENT."""
        self.status = MessageStatusEnum.SENT
        self.update_timestamp()

    def mark_as_failed(self):
        """Marks the message as FAILED."""
        self.status = MessageStatusEnum.FAILED
        self.update_timestamp()
