from typing import Optional
from app.repositories.user_repository import UserRepository
from app.domain.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserCreate


class UserService:
    def __init__(self, db: AsyncSession):
        self.repo = UserRepository(db)

    async def create_user(self, user_create: UserCreate, current_user: Optional[str] = None) -> User:
        new_user = User(
            username=user_create.username,
            email=user_create.email,
            hashed_password=user_create.password,
        )
        return await self.repo.create_user(new_user, current_user=current_user)

    async def get_user_by_username(self, username: str) -> Optional[User]:
        return await self.repo.get_user_by_username(username)