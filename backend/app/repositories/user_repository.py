from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.domain.user import User
from app.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository):
    def __init__(self, db: AsyncSession):
        super().__init__(db)  # Initialize BaseRepository with db session

    # create new user
    async def create_user(self, user: User, current_user: Optional[str] = None):
        try:
            self.db_session.add(user)
            await self.db_session.commit(current_user=current_user)  # Pass current user to session
            await self.db_session.refresh(user)
            return user
        except Exception as e:
            await self.db_session.rollback()
            print(f"Error: {e}")
            raise

    # update user
    async def update_user(self, user_id: int, user_update: User) -> Optional[User]:
        """
        Update a user's fields based on the provided updates.

        :param user_id: ID of the user to update.
        :param updates: Dictionary of fields to update.
        :return: The updated User object, or None if user does not exist.
        """
        try:
            result = await self.db_session.execute(select(User).where(User.id == user_id))
            user = result.scalar_one_or_none()
            if user is None:
                return  None

            # Apply updates from user_update to the fetched user
            if user_update.user_name is not None:
                user.user_name = user_update.user_name
            if user_update.email is not None:
                user.email = user_update.email
            if user_update.first_name is not None:
                user.first_name = user_update.first_name
            if user_update.last_name is not None:
                user.last_name = user_update.last_name
            if user_update.status is not None:
                user.status = user_update.status
            if user_update.is_email_verified is not None:
                user.is_email_verified = user_update.is_email_verified

            # Commit the changes to the database
            await self.db_session.commit()

            # Refresh the user instance to get the latest data from the database
            await self.db_session.refresh(user)
            return user
        except Exception as e:
            self.db_session.rollback()
            print(f"Error updating user: {e}")
            raise

    # delete user
    async def delete_user(self, user_id: int) -> bool:
        try:
            result = await self.db_session.execute(select(User).where(User.id == user_id))
            user = result.scalar_one_or_none()
            if user is None:
                return False

            await self.db_session.delete(user)
            await self.db_session.commit()
            return True
        except Exception as e:
            self.db_session.rollback()
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
        user = await self.db_session.get(User, user_id)
        if user is None:
            return None

        user.hashed_password = hashed_password

        try:
            await self.db_session.commit()
            await self.db_session.refresh(user)
            return True
        except Exception as e:
            await self.db_session.rollback()
            print(f"Error updating password: {e}")
            raise


    # get user by email
    async def get_user_by_email(self, email: str):
        result = await self.db_session.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    # get user by username
    async def get_user_by_username(self, username: str):
        result = await self.db_session.execute(select(User).where(User.user_name == username))
        return result.scalar_one_or_none()

    # # get all users
    # async def get_all_users(self, skip: int = 0, limit: int = 10) -> List[User]:
    #     """
    #     Fetch all users with optional pagination.
    #
    #     :param skip: Number of records to skip (default: 0).
    #     :param limit: Maximum number of records to return (default: 10).
    #     :return: List of User objects.
    #     """
    #     try:
    #         query = select(User).offset(skip).limit(limit)
    #         result = await self.db.execute(query)
    #         return result.scalars().all() # Return paginated users as a list
    #         return users.scal
    #     except Exception as e:
    #         print(f"Error fetching users: {e}")
    #         raise

    # get all users with pagination
    async def get_paginated_users(self, page: int = 1, page_size: int = 10) -> List[User]:
        """
        Fetch all users with optional pagination.

        :param page: The page number (default: 1).
        :param page_size: The number of users per page (default: 10).
        :return: List of User objects.
        """
        return await self.get_paginated(User, page=page, page_size=page_size)
