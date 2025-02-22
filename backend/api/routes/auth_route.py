from fastapi import APIRouter, Depends, HTTPException, status, Form
from sqlalchemy.ext.asyncio import AsyncSession
from core.infrastructure.database import get_db
from modules.auth.auth_dto import LoginResponse, LoginRequest, VerifyRequest, VerifyResponse
from modules.auth.auth_service import AuthService
from modules.user.user_dto import UserCreate, UserRead

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
        auth_service = AuthService(db)
        new_user = await auth_service.user_register(user_create=user_create)
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

@router.post("/verify_code/", response_model=VerifyResponse)
async def login(
    verify_request: VerifyRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Authenticate the user and return an access token and refresh token.
    """
    service = AuthService(db)
    return await service.verify_code(verify_request)