import os
from celery import Celery
from celery.schedules import crontab
from dotenv import load_dotenv
from workers.celery_worker import process_outbox  # Import Celery task

# Load environment variables
load_dotenv()

# Secure Redis URL
REDIS_URL = os.getenv("REDIS_URL")

# Initialize Celery for Beat
celery = Celery("tasks", broker=REDIS_URL, backend=REDIS_URL)

# Use Redis as the scheduler
celery.conf.beat_scheduler = "celery.beat.PersistentScheduler"

# Schedule periodic tasks
celery.conf.beat_schedule = {
    "process_outbox_every_min": {
        "task": "process_outbox",
        "schedule": crontab(minute="*/1"),  # Runs every minute
    },
}

celery.conf.timezone = "UTC"  # Set timezone for scheduling
if __name__ == "__main__":
    celery.start()