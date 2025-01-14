from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.user import UserRead, UserCreate
from app.services.user_service import UserService

router = APIRouter()

@router.post("/users/", response_model=UserRead)
async def create_user(
    user_create: UserCreate,  # Use the Pydantic schema
    db: AsyncSession = Depends(get_db),
):
    service = UserService(db)

    existing_user = await service.get_user_by_username(user_create.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")

    user = await service.create_user(user_create=user_create)
    return user