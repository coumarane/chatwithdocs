from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.domain.user import User


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_by_username(self, username: str):
        result = await self.db.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()

    async def create_user(self, user: User, current_user: Optional[str] = None):
        try:
            self.db.add(user)
            await self.db.commit(current_user=current_user)  # Pass current user to session
            await self.db.refresh(user)
            return user
        except Exception as e:
            await self.db.rollback()
            print(f"Error: {e}")
            raise