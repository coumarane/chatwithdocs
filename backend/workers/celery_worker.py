import asyncio
from app.core.infrastructure.database import async_session
from celery import Celery
from app.repositories.outbox_message_repository import OutboxMessageRepository
from app.services.outbox_message_service import OutboxMessageService

# REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "PassWord123")
REDIS_URL = f"redis://:PassWord123@localhost:6379/0"
# REDIS_URL = f"redis://:{REDIS_PASSWORD}@redis-server:6379/0"


celery = Celery(
    "tasks",
    broker=REDIS_URL,
    backend=REDIS_URL
)
#
@celery.task(name='all_task_done', bind=True, ignore_result=True)
def process_outbox(self):
    """ Celery task to process pending outbox messages (Async Inside Sync) """
    asyncio.run(_async_process_outbox())

async def _async_process_outbox():
    """ Actual async function for processing outbox messages """
    async with async_session() as db_session:
        async with db_session.begin():  # Ensure transaction is active
            print(f"DEBUG[_async_process_outbox]: db_session type in Celery: {type(db_session)}")
            outbox_repo = OutboxMessageRepository(db_session)
            outbox_service = OutboxMessageService(outbox_repo)
            await outbox_service.process_pending_messages()
#
# from celery.schedules import crontab
#
# celery.conf.beat_schedule = {
#     "process_outbox_every_minute": {
#         "task": "process_outbox",
#         "schedule": crontab(minute="*"),  # Runs every minute
#     }
# }


result = process_outbox.delay()
print(result.id)

