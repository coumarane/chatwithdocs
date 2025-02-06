from email.message import EmailMessage
from fastapi import HTTPException
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.core.config import settings
import aiosmtplib

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
    message = EmailMessage()
    message["From"] = settings.MAIL_FROM
    message["To"] = request.to_email
    message["Subject"] = request.subject
    message.set_content(request.body)

    try:
        await aiosmtplib.send(
            message,
            hostname=settings.MAIL_SERVER,
            port=settings.MAIL_PORT
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Email sending failed: {e}")

    return {"status": "email sent successfully"}