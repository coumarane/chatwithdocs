from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.services.auth_service import AuthService
from app.schemas.auth import LoginResponse, LoginRequest

router = APIRouter(tags=["authentication"])

@router.post("/login/", response_model=LoginResponse)
async def login(
    login_request: LoginRequest,
    db: AsyncSession = Depends(get_db),
):
    service = AuthService(db)
    return await service.login(login_request)
