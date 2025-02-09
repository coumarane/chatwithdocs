from app.core.email.send_email_verification import send_email_verification
from app.repositories.outbox_message_repository import OutboxMessageRepository
from sqlalchemy.ext.asyncio import AsyncSession
import json

class OutboxMessageService:
    def __init__(self, db: AsyncSession):
        self.repo = OutboxMessageRepository(db)

    async def store_user_registration_event(self, user_id: str, email: str, verification_code: str):
        """ Stores user registration email event in the outbox """
        payload = {
            "user_id": str(user_id),
            "email": email,
            "verification_code": str(verification_code)
        }
        await self.repo.add_message("USER_REGISTERED", payload)

    async def process_pending_messages(self):
        """ Processes all pending outbox messages """
        pending_messages = await self.repo.get_pending_messages()

        for message in pending_messages:
            payload = json.loads(message.payload)

            try:
                if message.event_type == "USER_REGISTERED":
                    await send_email_verification(payload["email"], payload["verification_code"])

                # Mark message as SENT
                await self.repo.mark_message_as_sent(message.id)

            except Exception as e:
                print(f"❌ Failed to process message {message.id}: {str(e)}")
                await self.repo.mark_message_as_failed(message.id)
