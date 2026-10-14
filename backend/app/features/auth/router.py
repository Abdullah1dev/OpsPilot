
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.features.auth.schemas import (
    TokenResponse,
    UserRegister,
    UserResponse,
    UserLogin,
)
from app.features.auth.service import register_user, login_user
from app.infrastructure.database.session import get_db


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    user_data: UserRegister,
    db: Session = Depends(get_db),
) -> UserResponse:
    """Register a new user account."""
    return register_user(db, user_data)


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    credentials: UserLogin,
    db: Session = Depends(get_db),
) -> TokenResponse:
    """Authenticate a user and return an access token."""
    return login_user(db, credentials)
