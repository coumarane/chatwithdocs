from datetime import datetime, timedelta
from fastapi import HTTPException, status
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.repositories.user_repository import UserRepository
from app.schemas.auth import LoginRequest, LoginResponse
from app.schemas.user import UserRead
from app.utils.password import verify_password
from app.core.security import create_access_token, create_refresh_token
from jose import JWTError, jwt

ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_MINUTES = 1440  # 1 day

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    def __init__(self, db: AsyncSession):
        self.repo = UserRepository(db)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verify that the plain password matches the hashed password.
        """
        return pwd_context.verify(plain_password, hashed_password)

    def create_access_token(self, data: dict, expires_delta: timedelta) -> str:
        """
        Create a JWT token with the given data and expiration.
        """
        to_encode = data.copy()
        expire = datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

    async def login(self, login_request: LoginRequest) -> LoginResponse:
        """
        Authenticate the user and return a JWT token if successful.
        """
        user = await self.repo.get_user_by_email(login_request.email)
        if not user or not verify_password(login_request.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Generate access token
        access_token = create_access_token(
            data={"sub": user.user_name, "token_type": "access"},
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        )

        # Generate refresh token
        refresh_token = create_refresh_token(
            data={"sub": user.user_name, "token_type": "refresh"},
            expires_delta=timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES),
        )

        # Ensure the user is converted to the Pydantic model
        user_read = UserRead.model_validate(user)

        return LoginResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            user=user_read,
        )
