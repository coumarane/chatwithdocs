import os
import mimetypes
from dataclasses import dataclass
from email.message import EmailMessage
from typing import List, Optional, Union
import aiosmtplib

@dataclass
class Attachment:
    """
    Represents an attachment file provided in memory.
    """
    filename: str
    content: bytes
    mime_type: Optional[str] = None

class MailManagerException(Exception):
    """Custom exception class for MailManager errors."""
    pass


class MailManager:
    """
    A class to manage sending emails with optional attachments and alternative content (plain text or HTML).
    """

    def __init__(self, mail_server: str, mail_port: int, mail_from: str):
        """
        Initialize the MailManager with SMTP configuration.

        :param mail_server: The SMTP server hostname.
        :param mail_port: The SMTP server port.
        :param mail_from: The sender email address.
        """
        self.mail_server = mail_server
        self.mail_port = mail_port
        self.mail_from = mail_from

    async def send_email(
        self,
        to_email: str,
        subject: str,
        body: str,
        body_type: str = "plain",
        attachments: Optional[List[Union[str, Attachment]]] = None,
    ) -> dict:
        """
        Send an email with optional attachments.

        :param to_email: Recipient email address.
        :param subject: Email subject.
        :param body: Email body content.
        :param body_type: The content type of the body ('plain' or 'html').
        :param attachments: A list of file paths to attach to the email.
        :return: A dict containing the status of the email sending.
        :raises MailManagerException: If any error occurs during file handling or sending.
        """
        # Create an instance of EmailMessage
        message = EmailMessage()
        message["From"] = self.mail_from
        message["To"] = to_email
        message["Subject"] = subject

        # Set the email content based on the body type.
        if body_type.lower() == "html":
            # When sending HTML content, add an HTML alternative.
            message.add_alternative(body, subtype="html")
        else:
            message.set_content(body)

        # Process any attachments
        if attachments:
            for att in attachments:
                # If the attachment is a string, treat it as a file path.
                if isinstance(att, str):
                    file_path = att
                    if not os.path.isfile(file_path):
                        raise MailManagerException(f"Attachment not found: {file_path}")
                    try:
                        with open(file_path, "rb") as f:
                            file_data = f.read()
                    except Exception as e:
                        raise MailManagerException(f"Error reading attachment {file_path}: {e}")

                    filename = os.path.basename(file_path)
                    # Guess the MIME type
                    ctype, encoding = mimetypes.guess_type(file_path)
                    if ctype is None or encoding is not None:
                        ctype = "application/octet-stream"
                    maintype, subtype = ctype.split("/", 1)
                    message.add_attachment(
                        file_data,
                        maintype=maintype,
                        subtype=subtype,
                        filename=filename,
                    )
                # If the attachment is an Attachment instance, use its content directly.
                elif isinstance(att, Attachment):
                    filename = att.filename
                    file_data = att.content
                    # Determine MIME type: use provided mime_type or guess based on filename.
                    if att.mime_type:
                        ctype = att.mime_type
                    else:
                        ctype, _ = mimetypes.guess_type(filename)
                        if ctype is None:
                            ctype = "application/octet-stream"
                    maintype, subtype = ctype.split("/", 1)
                    message.add_attachment(
                        file_data,
                        maintype=maintype,
                        subtype=subtype,
                        filename=filename,
                    )
                else:
                    raise MailManagerException("Attachment must be a file path (str) or an Attachment instance.")

        # Send the email asynchronously using aiosmtplib
        try:
            await aiosmtplib.send(
                message,
                hostname=self.mail_server,
                port=self.mail_port,
            )
        except Exception as e:
            raise MailManagerException(f"Email sending failed: {e}")

        return {"status": "success", "message": "email sent successfully"}
