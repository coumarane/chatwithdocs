from pydantic import BaseModel

from app.schemas.user import UserRead


class LoginRequest(BaseModel):
    email: str
    password: str

class TokenData(BaseModel):
    username: str | None = None

class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    user: UserRead


