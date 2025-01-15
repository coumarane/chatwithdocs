from typing import Optional, List
from app.repositories.user_repository import UserRepository
from app.domain.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserCreate, UserRead, UserUpdate
from passlib.context import CryptContext

# Initialize the password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    def __init__(self, db: AsyncSession):
        self.repo = UserRepository(db)

    async def create_user(self, user_create: UserCreate, current_user: Optional[str] = None) -> User:
        # Hash the user's password
        hashed_password = pwd_context.hash(user_create.password)

        new_user = User(
            username=user_create.username,
            email=user_create.email,
            hashed_password=hashed_password,
        )
        return await self.repo.create_user(new_user, current_user=current_user)

    # update user
    async def update_user(self, user_id: int, user_update: UserUpdate) -> Optional[UserRead]:
        """
        Update a user with the given data.

        :param user_id: ID of the user to update.
        :param user_update: UserUpdate schema with fields to update.
        :return: Updated UserRead object or None if user does not exist.
        """
        updates = user_update.model_dump(exclude_unset=True)
        updated_user = await self.repo.update_user(user_id, updates)
        if updated_user:
            return UserRead(id=updated_user.id, username=updated_user.username, email=updated_user.email)
        return None

    # delete user
    async def delete_user(self, user_id: int) -> bool:
        """
        Delete a user by ID.

        :param user_id: ID of the user to delete.
        :return: True if user was deleted, False otherwise.
        """
        return await self.repo.delete_user(user_id)

    # update user password
    async def update_password(self, user_id: int, new_password: str) -> bool:
        # Hash the user's password
        hashed_password = pwd_context.hash(new_password)

        updated_user = await self.repo.update_password(user_id, hashed_password)
        if updated_user:
            return True
        return False

    async def get_user_by_username(self, username: str) -> Optional[User]:
        return await self.repo.get_user_by_username(username)

    async def get_all_users(self, skip: int = 0, limit: int = 10) -> List[UserRead]:
        users = await self.repo.get_all_users(skip=skip, limit=limit)
        return [UserRead(id=user.id, username=user.username, email=user.email) for user in users]