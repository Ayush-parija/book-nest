from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import decode_token

from app.core.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_password,
)
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import LoginRequest, SignupRequest


def create_user(data: SignupRequest, db: Session) -> User:

    existing = UserRepository.get_by_email(data.email, db)

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Email already registered",
        )

    user = User(
        name=data.name,
        email=data.email,
        password_hash=hash_password(data.password),
    )

    return UserRepository.create(user, db)


def login_user(data: LoginRequest, db: Session) -> dict:
    user = UserRepository.get_by_email(data.email, db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    if not verify_password(
        data.password,
        user.password_hash,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    return {
        "access_token": create_access_token(user.id),
        "refresh_token": create_refresh_token(user.id),
        "token_type": "bearer",
    }

def refresh_access_token(data):
    payload = decode_token(data.refresh_token)

    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token",
        )

    if payload.get("type") != "refresh":
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token",
        )

    user_id = int(payload["sub"])

    return {
        "access_token": create_access_token(user_id),
        "token_type": "bearer",
    }


def logout_user():
    return {
        "message": "Logged out successfully"
    }