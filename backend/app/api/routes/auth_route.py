from fastapi import APIRouter, Depends, HTTPException, status, Form
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.oauth2password_request_form import OAuth2PasswordRequestFormEmail
from app.schemas.user import UserRead, UserCreate
from app.services.auth_service import AuthService
from app.schemas.auth import LoginResponse, LoginRequest
from fastapi.security import OAuth2PasswordRequestForm

from app.services.user_service import UserService

router = APIRouter(tags=["authentication"])

@router.post("/token/", response_model=LoginResponse)
async def login(
    email: str = Form(...),  # Use Form to accept 'email'
    password: str = Form(...),  # Use Form to accept 'password',
    db: AsyncSession = Depends(get_db),
):
    """
    Authenticate the user and return an access token and refresh token.
    """
    service = AuthService(db)
    login_request = LoginRequest(email=email, password=password)
    return await service.login(login_request)

@router.post("/register", response_model=UserRead)
async def register(
    user_create: UserCreate,  # Use the Pydantic schema
    db: AsyncSession = Depends(get_db)):

    try:
        service = UserService(db)

        existing_user = await service.get_user_by_username(user_create.username)
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already taken")

        new_user = await service.create_user(user_create=user_create)
        return new_user
    except Exception as e:
        # You could customize error handling here
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/login/", response_model=LoginResponse)
async def login(
    login_request: LoginRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Authenticate the user and return an access token and refresh token.
    """
    service = AuthService(db)
    return await service.login(login_request)