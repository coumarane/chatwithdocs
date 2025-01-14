from pydantic import BaseModel

class LoginRequest(BaseModel):
    username: str
    password: str


class TokenData(BaseModel):
    username: str | None = None

class LoginResponse(TokenData):
    access_token: str
    refresh_token: str
    token_type: str


