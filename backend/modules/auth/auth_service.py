from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException, status
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from core.config.config import settings
from core.security.security import create_access_token, create_refresh_token
from core.utils.password import verify_password
from jose import jwt
from modules.auth.auth_dto import LoginResponse, LoginRequest, VerifyRequest
from modules.outbox_message.outbox_message_service import OutboxMessageService
from modules.user.user import User
from modules.user.user_dto import UserCreate, UserRead
from modules.user.user_repository import UserRepository

ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_MINUTES = 1440  # 1 day

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    def __init__(self, db: AsyncSession):
        self.repo = UserRepository(db)
        self.outbox_service = OutboxMessageService(db)

    async def user_register(self, user_create: UserCreate, current_user: Optional[str] = None) -> User:

        existing_user = await self.repo.get_user_by_username(user_create.username)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )

        # User exists
        user_email_exists = await self.repo.get_user_by_email(user_create.email)
        if user_email_exists:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User with email already exists"
            )

        if not user_create.hasAgreedTerms:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User must agree to the terms and privacy policy."
            )

        # Hash the user's password
        hashed_password = pwd_context.hash(user_create.password)
        new_user = User(
            user_name=user_create.username,
            email=user_create.email,
            hashed_password=hashed_password,
            has_agreed_terms=user_create.hasAgreedTerms
        )

        # Create user in DB (atomic transaction)
        registred_user = await self.repo.create_user(new_user, current_user=current_user)
        user = registred_user.to_domain()

        verification_code = user.verification_token
        await self.outbox_service.store_user_registration_event(user.id, user_create.email, verification_code)

        return user

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

    async def verify_code(self, request: VerifyRequest):
        user = self.repo.get_user_by_email(request.email)

        if not user or user["code"] != request.code:
            raise HTTPException(status_code=400, detail="Invalid verification code")

        # TODO: Update user table email_verified = true

        return {"message": "Email verified successfully"}
