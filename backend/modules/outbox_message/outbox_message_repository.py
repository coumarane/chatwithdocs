from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update
import json
from sqlalchemy.orm import selectinload
from core.infrastructure.base_repository import BaseRepository
from modules.outbox_message.message_status_enum import MessageStatusEnum
from modules.outbox_message.outbox_message import OutboxMessage
from modules.outbox_message.outbox_message_orm import OutboxMessageORM


class OutboxMessageRepository(BaseRepository):
    def __init__(self, db: AsyncSession):
        super().__init__(db)  # Initialize BaseRepository with db session

    async def add_message(self, event_type: str, payload: dict) -> OutboxMessageORM:
        """ Inserts a new message into the outbox table """
        message = OutboxMessageORM(
            event_type=event_type,
            payload=json.dumps(payload),
            status=MessageStatusEnum.PENDING.value
        )
        self.db_session.add(message)
        await self.db_session.commit()
        await self.db_session.refresh(message)  # Refresh to get the new ID and state
        return message

    async def get_pending_messages(self) -> list[OutboxMessageORM]:
        """ Fetch all pending messages as ORM objects """
        result = await self.db_session.execute(
            select(OutboxMessageORM)
            .where(OutboxMessageORM.status == MessageStatusEnum.PENDING.value)
            .options(selectinload(OutboxMessageORM))  # Optimized for relationship loading
        )
        return result.scalars().all()  # Returns ORM instances

    async def mark_message_as_sent(self, message_id: int) -> None:
        """ Mark a message as SENT """
        await self.db_session.execute(
            update(OutboxMessageORM)
            .where(OutboxMessageORM.id == message_id)
            .values(status=MessageStatusEnum.SENT.value)
        )
        await self.db_session.commit()

    async def mark_message_as_failed(self, message_id: int) -> None:
        """ Mark a message as FAILED """
        await self.db_session.execute(
            update(OutboxMessageORM)
            .where(OutboxMessageORM.id == message_id)
            .values(status=MessageStatusEnum.FAILED.value)
        )
        await self.db_session.commit()
