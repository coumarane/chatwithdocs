import os
import asyncio
from dotenv import load_dotenv
from core.infrastructure.database import async_session
from celery import Celery
from modules.outbox_message.outbox_message_service import OutboxMessageService

# Load environment variables from a .env file
load_dotenv()

REDIS_URL = os.getenv("REDIS_URL")


celery = Celery(
    "tasks",
    broker=REDIS_URL,
    backend=REDIS_URL
)

@celery.task(name='process_outbox')
def process_outbox():
    """ Celery sync wrapper to call the async function. """
    asyncio.run(_async_process_outbox())

async def _async_process_outbox():
    """ Actual async function for processing outbox messages """
    async with async_session() as db_session:
        async with db_session.begin():  # Ensure transaction is active
            print(f"DEBUG[_async_process_outbox]: db_session type in Celery: {type(db_session)}")
            outbox_service = OutboxMessageService(db_session)
            await outbox_service.process_pending_messages()

