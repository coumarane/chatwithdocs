from app.repositories.user_repository import UserRepository
from app.domain.user import User

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def create_user(self, username: str, email: str, hashed_password: str):
        user = User(username=username, email=email, hashed_password=hashed_password)
        return await self.user_repository.create_user(user)

    async def get_user_by_username(self, username: str):
        return await self.user_repository.get_user_by_username(username)