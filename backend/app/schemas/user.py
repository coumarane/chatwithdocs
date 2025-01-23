from uuid import UUID

from pydantic import BaseModel, EmailStr, model_validator


# User Create Model
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

# User Read Model
from pydantic import BaseModel, EmailStr, model_validator
from uuid import UUID  # Import UUID from the uuid module

class UserRead(BaseModel):
    id: UUID
    username: str
    email: EmailStr

    @model_validator(mode="before")  # Use the new style model_validator with mode="before"
    def check_username(cls, values):
        # Check if the 'user_name' attribute exists in the model instance, and map it to 'username'
        if hasattr(values, 'user_name'):
            values.username = values.user_name  # Map 'user_name' to 'username'
        return values

    model_config = {
        "from_attributes": True  # Enables attribute mapping from ORM objects
    }


# User Update Model
class UserUpdate(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
