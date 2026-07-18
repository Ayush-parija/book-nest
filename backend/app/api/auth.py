from fastapi import APIRouter, Cookie, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from typing import Optional

from app.dependencies.auth import get_current_user
from app.models.user import User

from fastapi.security import OAuth2PasswordRequestForm

from app.dependencies.database import get_db
from app.schemas.auth import (
    SignupRequest,
    AccessTokenResponse,
)
from app.services.auth_service import (
    create_user,
    login_user,
)
from app.core.security import decode_token, create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post("/signup")
def signup(
    data: SignupRequest,
    db: Session = Depends(get_db),
):
    user = create_user(data, db)

    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
    }


@router.post("/login")
def login(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """
    Authenticate the user.
    - Returns access_token in the JSON body (stored in localStorage by client).
    - Sets refresh_token as a secure HttpOnly cookie (not accessible from JS, safer against XSS).
    """
    from app.schemas.auth import LoginRequest

    tokens = login_user(
        LoginRequest(
            email=form_data.username,
            password=form_data.password,
        ),
        db,
    )

    # Set refresh token as HttpOnly cookie — browser sends it automatically
    response.set_cookie(
        key="refresh_token",
        value=tokens["refresh_token"],
        httponly=True,              # Not accessible from JavaScript
        samesite="lax",            # Protect against CSRF
        max_age=7 * 24 * 60 * 60,  # 7 days in seconds
        path="/auth",              # Only sent to /auth/* endpoints
    )

    return {
        "access_token": tokens["access_token"],
        "token_type": "bearer",
    }


@router.get("/me")
def me(
    current_user: User = Depends(get_current_user),
):
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
    }


@router.post(
    "/refresh",
    response_model=AccessTokenResponse,
)
def refresh_token(
    refresh_token: Optional[str] = Cookie(default=None),
):
    """
    Issues a new access token using the HttpOnly refresh_token cookie.
    The client sends NO body — the cookie is read automatically by the browser.
    """
    if not refresh_token:
        raise HTTPException(
            status_code=401,
            detail="Refresh token not found. Please log in again.",
        )

    payload = decode_token(refresh_token)

    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired refresh token. Please log in again.",
        )

    if payload.get("type") != "refresh":
        raise HTTPException(
            status_code=401,
            detail="Invalid token type.",
        )

    user_id = int(payload["sub"])

    return {
        "access_token": create_access_token(user_id),
        "token_type": "bearer",
    }


@router.post("/logout")
def logout(response: Response):
    """
    Clears the HttpOnly refresh_token cookie on the server.
    The client should also remove the access token from localStorage.
    """
    response.delete_cookie(
        key="refresh_token",
        path="/auth",
    )
    return {"message": "Logged out successfully"}