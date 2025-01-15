from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.domain import User
from app.schemas.user import UserRead, UserCreate, UserUpdate
from app.services.user_service import UserService

router = APIRouter()

@router.get("/profile/")
async def read_users_me(current_user: User = Depends(get_current_user)):
    """
    Get the current user's profile.
    """
    return {"username": current_user.username, "email": current_user.email}

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

@router.put("/users/{user_id}", response_model=UserRead)
async def update_user(user_id: int, user_update: UserUpdate, db: AsyncSession = Depends(get_db)):
    service = UserService(db)

    updated_user = await service.update_user(user_id, user_update)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@router.delete("/users/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user_service = UserService(db)
    success = await user_service.delete_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted successfully"}

@router.patch("/users/{user_id}/password")
async def update_password(user_id: int, new_password: str, db: AsyncSession = Depends(get_db)):
    """
    Endpoint to update a user's password.

    :param user_id: ID of the user.
    :param new_password: The new plain-text password.
    :param db: Database session.
    """
    user_service = UserService(db)
    updated_user = await user_service.update_password(user_id, new_password)
    if updated_user is False:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "Password updated successfully"}

@router.get("/users", response_model=List[UserRead])
async def get_users(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    user_service = UserService(db)
    return await user_service.get_all_users(skip=skip, limit=limit)