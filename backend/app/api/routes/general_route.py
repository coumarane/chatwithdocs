from email.message import EmailMessage
from fastapi import HTTPException
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.core.config import settings
import aiosmtplib

from app.core.email.mail_manager import MailManager
from app.schemas.email import EmailRequest

templates = Jinja2Templates(directory="app/templates")
router = APIRouter()

@router.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/test")
def get_test():
    return {"Hello": "World"}


@router.post("/send-email")
async def send_email(request: EmailRequest):
    # Create an instance of MailManager
    mail_manager = MailManager(
        mail_server = settings.MAIL_SERVER,
        mail_port = settings.MAIL_PORT,
        mail_from = settings.MAIL_FROM
    )

    result = await mail_manager.send_email(
        to_email = request.to_email,
        subject = request.subject,
        body = request.body
        # body="<h1>Hello, World!</h1>",
        # body_type="html",
        # attachments=["/path/to/attachment.pdf"],
    )
    return result
