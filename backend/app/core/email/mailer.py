from typing import List
from pydantic import EmailStr, BaseModel

class EmailSchema(BaseModel):
    email: List[EmailStr]

# conf = ConnectionConfig(
#     MAIL_USERNAME = "username",
#     MAIL_PASSWORD = "**********",
#     MAIL_FROM = "test@email.com",
#     MAIL_PORT = 587,
#     MAIL_SERVER = "mail server",
#     MAIL_FROM_NAME="Desired Name",
#     MAIL_STARTTLS = True,
#     MAIL_SSL_TLS = False,
#     USE_CREDENTIALS = True,
#     VALIDATE_CERTS = True
# )


def send_mail_test():
    pass