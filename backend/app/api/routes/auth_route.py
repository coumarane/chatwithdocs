from fastapi import APIRouter, Depends, HTTPException, status, Form
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.oauth2password_request_form import OAuth2PasswordRequestFormEmail
from app.services.auth_service import AuthService
from app.schemas.auth import LoginResponse, LoginRequest
from fastapi.security import OAuth2PasswordRequestForm

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