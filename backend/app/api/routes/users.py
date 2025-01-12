from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_db
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService

router = APIRouter()

@router.post("/users/")
async def create_user(
    username: str,
    email: str,
    password: str,
    db: AsyncSession = Depends(get_db),
):
    user_repository = UserRepository(db)
    user_service = UserService(user_repository)

    existing_user = await user_service.get_user_by_username(username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")

    # Hash password
    hashed_password = f"hashed-{password}"
    user = await user_service.create_user(username, email, hashed_password)
    return {"id": user.id, "username": user.username, "email": user.email}