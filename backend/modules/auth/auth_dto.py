from pydantic import BaseModel
from modules.user.user_dto import UserRead

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

class VerifyRequest(BaseModel):
    email: str
    code: str

