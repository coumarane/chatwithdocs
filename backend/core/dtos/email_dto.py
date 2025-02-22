from pydantic import BaseModel, EmailStr
from typing import Optional, List

class EmailRequest(BaseModel):
    to_email: EmailStr
    subject: str
    body: str
    body_type: Optional[str] = "plain"  # 'plain' or 'html'
    attachments: Optional[List[str]] = None  # List of file paths for attachments