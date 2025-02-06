from app.core.config import settings
from app.core.email.mail_manager import MailManager


async def send_email_verification(to_email: str, verification_code: str):
    content = f"""
            Hello, {to_email}

            To continue setting up your account, please verify your account with the code below:

            {verification_code}

            This code will expire in 5 days.

            Click the link below to verify:
            https://chatwithdocs.com/auth/verify-code
        """

    # Create an instance of MailManager
    mail_manager = MailManager(
        mail_server = settings.MAIL_SERVER,
        mail_port = settings.MAIL_PORT,
        mail_from = settings.MAIL_FROM
    )

    result = await mail_manager.send_email(
        to_email = to_email,
        subject = "Verify Your Email for ChatWithDocs Registration",
        body = content
    )

    return result