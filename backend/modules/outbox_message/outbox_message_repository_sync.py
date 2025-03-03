from sqlalchemy.future import select
from sqlalchemy import update
import json
from sqlalchemy.orm import Session
from modules.outbox_message.message_status_enum import MessageStatusEnum
from modules.outbox_message.outbox_message_orm import OutboxMessageORM


class OutboxMessageRepositorySync():
    def __init__(self, db: Session):
        self.db_session = db

    def add_message(self, event_type: str, payload: dict) -> OutboxMessageORM:
        """ Inserts a new message into the outbox table """
        message = OutboxMessageORM(
            event_type=event_type,
            payload=json.dumps(payload),
            status=MessageStatusEnum.PENDING.value
        )
        self.db_session.add(message)
        self.db_session.commit()
        self.db_session.refresh(message)  # Refresh to get the new ID and state
        return message

    def get_pending_messages(self) -> list[OutboxMessageORM]:
        """Fetch all pending messages safely."""
        result = self.db_session.execute(
            select(OutboxMessageORM).where(OutboxMessageORM.status == MessageStatusEnum.PENDING.value)
        )
        messages = result.scalars().all()
        return messages or []  # Ensure it returns an empty list, not None

    def mark_message_as_sent(self, message_id: int) -> None:
        """ Mark a message as SENT """
        try:
            self.db_session.execute(
                update(OutboxMessageORM)
                .where(OutboxMessageORM.id == message_id)
                .values(status=MessageStatusEnum.SENT.value)
            )
            self.db_session.commit()
        except:
            self.db_session.rollback()
            raise

    def mark_message_as_failed(self, message_id: int) -> None:
        try:
            self.db_session.execute(
                update(OutboxMessageORM)
                .where(OutboxMessageORM.id == message_id)
                .values(status=MessageStatusEnum.FAILED.value)
            )
            self.db_session.commit()
        except:
            self.db_session.rollback()
            raise
