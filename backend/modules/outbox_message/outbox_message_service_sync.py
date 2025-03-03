import json
import logging
from sqlalchemy.orm import Session
from core.email.send_email_verification import send_email_verification
from modules.outbox_message.outbox_message_repository_sync import OutboxMessageRepositorySync
from asgiref.sync import async_to_sync

logger = logging.getLogger(__name__)

class OutboxMessageServiceSync:
    def __init__(self, db: Session):
        self.repo = OutboxMessageRepositorySync(db)

    def store_user_registration_event(self, user_id: str, email: str, verification_code: str):
        """ Stores user registration email event in the outbox """
        payload = {
            "user_id": str(user_id),
            "email": email,
            "verification_code": str(verification_code)
        }
        message = self.repo.add_message("USER_REGISTERED", payload)
        logger.info(f"✅ Stored USER_REGISTERED event in outbox (ID: {message.id})")
        return message

    def process_pending_messages(self):
        """ Processes all pending outbox messages """
        pending_messages = self.repo.get_pending_messages()

        for message in pending_messages:
            payload = json.loads(message.payload)

            try:
                logger.info(f"📨 Processing message ID {message.id} (Event: {message.event_type})")

                if message.event_type == "USER_REGISTERED":
                    async_to_sync(send_email_verification)(payload["email"], payload["verification_code"])
                    # Mark message as SENT
                    self.repo.mark_message_as_sent(message.id)
                    logger.info(f"✅ Successfully processed message ID {message.id}")

            except Exception as e:
                logger.error(f"❌ Failed to process message {message.id}: {str(e)}", exc_info=True)

                # You could also mark the message as FAILED if needed
                self.repo.mark_message_as_failed(message.id)
