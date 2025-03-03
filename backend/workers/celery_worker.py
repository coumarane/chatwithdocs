import os
import asyncio
from dotenv import load_dotenv
from core.infrastructure.database import get_sync_db
from celery import Celery
from modules.outbox_message.outbox_message_service import OutboxMessageService
from modules.outbox_message.outbox_message_service_sync import OutboxMessageServiceSync

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
    """ Celery sync task using sync DB session. """
    for db_session in get_sync_db():
        print(f"DEBUG[process_outbox]: db_session type in Celery: {type(db_session)}")

        outbox_service = OutboxMessageServiceSync(db_session)
        outbox_service.process_pending_messages()



