from typing import Optional, List

from pycparser.ply.yacc import resultlimit
from sqlalchemy import false
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.domain.user import User


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    # create new user
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

    # update user
    async def update_user(self, user_id: int, updates: dict) -> Optional[User]:
        """
        Update a user's fields based on the provided updates.

        :param user_id: ID of the user to update.
        :param updates: Dictionary of fields to update.
        :return: The updated User object, or None if user does not exist.
        """
        try:
            result = await self.db.execute(select(User).where(User.id == user_id))
            user = result.scalar_one_or_none()
            if user is None:
                return  None

            for key, value in updates.items():
                setattr(user, key, value)

            await self.db.commit()
            await self.db.refresh(user)
            return user
        except Exception as e:
            self.db.rollback()
            print(f"Error updating user: {e}")
            raise

    # delete user
    async def delete_user(self, user_id: int) -> bool:
        try:
            result = await self.db.execute(select(User).where(User.id == user_id))
            user = result.scalar_one_or_none()
            if user is None:
                return False

            await self.db.delete(user)
            await self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            print(f'')
            return False

    # update user password
    async def update_password(self, user_id: int, hashed_password: str) -> bool:
        """
        Update the user's password.

        :param user_id: ID of the user whose password is being updated.
        :param hashed_password: The new hashed password.
        :return: The updated User object or None if the user is not found.
        """
        user = await self.db.get(User, user_id)
        if user is None:
            return None

        user.hashed_password = hashed_password

        try:
            await self.db.commit()
            await self.db.refresh(user)
            return True
        except Exception as e:
            await self.db.rollback()
            print(f"Error updating password: {e}")
            raise


    # get user by email
    async def get_user_by_email(self, email: str):
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    # get user by username
    async def get_user_by_username(self, username: str):
        result = await self.db.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()

    # get all users
    async def get_all_users(self, skip: int = 0, limit: int = 10) -> List[User]:
        """
        Fetch all users with optional pagination.

        :param skip: Number of records to skip (default: 0).
        :param limit: Maximum number of records to return (default: 10).
        :return: List of User objects.
        """
        try:
            query = select(User).offset(skip).limit(limit)
            result = await self.db.execute(query)
            return result.scalars().all() # Return paginated users as a list
            return users.scal
        except Exception as e:
            print(f"Error fetching users: {e}")
            raise
