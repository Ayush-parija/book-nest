from fastapi import APIRouter, Cookie, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from typing import Optional

# Dependency to get the currently logged-in user
from app.dependencies.auth import get_current_user
from app.models.user import User

# Handles login form data (username & password)
from fastapi.security import OAuth2PasswordRequestForm

# Database session dependency
from app.dependencies.database import get_db

# Request and response schemas
from app.schemas.auth import (
    SignupRequest,
    AccessTokenResponse,
)

# Authentication service functions
from app.services.auth_service import (
    create_user,
    login_user,
)

# JWT helper functions
from app.core.security import decode_token, create_access_token

# Authentication router
router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


# Register a new user
@router.post("/signup")
def signup(
    data: SignupRequest,
    db: Session = Depends(get_db),
):
    # Create user in database
    user = create_user(data, db)

    # Return basic user details
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
    }


# Login endpoint
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

    # Verify credentials and generate tokens
    tokens = login_user(
        LoginRequest(
            email=form_data.username,
            password=form_data.password,
        ),
        db,
    )

    # Store refresh token in HttpOnly cookie
    response.set_cookie(
        key="refresh_token",
        value=tokens["refresh_token"],
        httponly=True,              # Prevent JavaScript access
        samesite="lax",             # Basic CSRF protection
        max_age=7 * 24 * 60 * 60,   # Cookie expires after 7 days
    )

    # Send access token to frontend
    return {
        "access_token": tokens["access_token"],
        "token_type": "bearer",
    }


# Get details of the currently logged-in user
@router.get("/me")
def me(
    current_user: User = Depends(get_current_user),
):
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
    }


# Generate a new access token using refresh token
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

    # Refresh token must exist
    if not refresh_token:
        raise HTTPException(
            status_code=401,
            detail="Refresh token not found. Please log in again.",
        )

    # Decode and validate refresh token
    payload = decode_token(refresh_token)

    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired refresh token. Please log in again.",
        )

    # Ensure this is actually a refresh token
    if payload.get("type") != "refresh":
        raise HTTPException(
            status_code=401,
            detail="Invalid token type.",
        )

    # Extract user id from token
    user_id = int(payload["sub"])

    # Return a newly generated access token
    return {
        "access_token": create_access_token(user_id),
        "token_type": "bearer",
    }


# Logout endpoint
@router.post("/logout")
def logout(response: Response):
    """
    Clears the HttpOnly refresh_token cookie on the server.
    The client should also remove the access token from localStorage.
    """

    # Remove refresh token cookie
    response.delete_cookie(
        key="refresh_token",
    )

    return {"message": "Logged out successfully"}