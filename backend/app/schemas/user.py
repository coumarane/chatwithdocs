from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr

    model_config = {
        "from_attributes": True  # Enables attribute mapping from ORM objects
    }


class UserUpdate(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
