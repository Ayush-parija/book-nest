# =========================================================
# File: auth_service.py
# Purpose:
# Handles all business logic related to user authentication.
#
# Responsibilities:
# - User signup and login
# - JWT token generation (access and refresh)
# - Password hashing and verification
# - Token refresh validation
#
# Depends on:
# - UserRepository
# - User model
# - Security core utilities (JWT, password hashing)
#
# Used by:
# - auth.py router
# =========================================================

# Navigation
# [1] Third-party Libraries
# [2] Local Models & Schemas
# [3] Repositories
# [4] Security Utilities
# [5] Authentication Logic

# =====================================================
# [1] Third-party Libraries
# =====================================================
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

# =====================================================
# [4] Security Utilities
# =====================================================
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)

# =====================================================
# [2] Local Models & Schemas
# =====================================================
from app.models.user import User
from app.schemas.auth import LoginRequest, SignupRequest

# =====================================================
# [3] Repositories
# =====================================================
from app.repositories.user_repository import UserRepository


# =====================================================
# [5] Authentication Logic
# =====================================================

def create_user(data: SignupRequest, db: Session) -> User:
    """
    ---------------------------------------------------------
    Function:
    create_user()

    Purpose:
    Creates a new user account with a hashed password.

    Parameters:
    data: SignupRequest object containing user details
    db: Database session

    Returns:
    User: The newly created User instance

    Raises:
    400 HTTPException: If the email is already registered

    Side Effects:
    - Inserts a new user record into the database
    ---------------------------------------------------------
    """
    existing = UserRepository.get_by_email(data.email, db)

    # Prevent duplicate email registration
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
    """
    ---------------------------------------------------------
    Function:
    login_user()

    Purpose:
    Authenticates a user and generates JWT tokens.

    Parameters:
    data: LoginRequest containing email and password
    db: Database session

    Returns:
    dict: Contains access_token, refresh_token, and token_type

    Raises:
    401 HTTPException: If the email or password is invalid

    Side Effects:
    None
    ---------------------------------------------------------
    """
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
    """
    ---------------------------------------------------------
    Function:
    refresh_access_token()

    Purpose:
    Issues a new access token using a valid refresh token.

    Parameters:
    data: Object containing the refresh_token

    Returns:
    dict: Contains new access_token and token_type

    Raises:
    401 HTTPException: If the refresh token is invalid or expired

    Side Effects:
    None
    ---------------------------------------------------------
    """
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
    """
    ---------------------------------------------------------
    Function:
    logout_user()

    Purpose:
    Handles business logic for logging out a user.

    Parameters:
    None

    Returns:
    dict: A success message

    Raises:
    None

    Side Effects:
    None (cookie deletion is handled by the router)
    ---------------------------------------------------------
    """
    return {
        "message": "Logged out successfully"
    }