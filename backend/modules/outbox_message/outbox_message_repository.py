from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update
import json
from core.infrastructure.base_repository import BaseRepository
from modules.outbox_message.outbox_message import OutboxMessage


class OutboxMessageRepository(BaseRepository):
    def __init__(self, db: AsyncSession):
        super().__init__(db)  # Initialize BaseRepository with db session

    async def add_message(self, event_type: str, payload: dict):
        """ Inserts a new message into the outbox table """
        message = OutboxMessage(event_type=event_type, payload=json.dumps(payload), status="PENDING")
        self.db_session.add(message)
        await self.db_session.commit()
        return message

    async def get_pending_messages(self):
        """ Fetch all pending messages """
        print(f"DEBUG[get_pending_messages]:: db_session type: {type(self.db_session)}")  # Should print <class 'AsyncSession'>
        result = await self.db_session.execute(
            select(OutboxMessage).where(OutboxMessage.status == "PENDING")
        )
        return result.scalars().all()

    async def mark_message_as_sent(self, message_id: int):
        """ Mark a message as SENT """
        await self.db_session.execute(update(OutboxMessage).where(OutboxMessage.id == message_id).values(status="SENT"))
        await self.db_session.commit()

    async def mark_message_as_failed(self, message_id: int):
        """ Mark a message as FAILED """
        await self.db_session.execute(update(OutboxMessage).where(OutboxMessage.id == message_id).values(status="FAILED"))
        await self.db_session.commit()
