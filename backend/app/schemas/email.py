from pydantic import BaseModel, EmailStr

class EmailRequest(BaseModel):
    to_email: EmailStr
    subject: str
    body: str