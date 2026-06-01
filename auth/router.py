import logging
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from auth import service as auth_service
from auth.schemas import TokenRefresh, TokenResponse
from database.connection import get_db

router = APIRouter(prefix="/auth", tags=["Auth"])
logger = logging.getLogger(__name__)


@router.post("/login", response_model=TokenResponse)
async def login(
    form: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
):

    token = await auth_service.login(db, form.username, form.password)
    logger.info(f"user {form.username}has been logged successfully")
    return TokenResponse(
        access_token=token["access_token"], refresh_token=token["refresh_token"]
    )


@router.post("/refresh")
async def refresh(body: TokenRefresh):
    token = await auth_service.refresh(body.refresh_token)

    return {"access_token": token}
