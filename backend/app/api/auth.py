from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies.auth import get_current_user
from app.models.user import User

from fastapi.security import OAuth2PasswordRequestForm

from app.dependencies.database import get_db
from app.schemas.auth import (
    LoginRequest,
    SignupRequest,
    TokenResponse,
)
from app.services.auth_service import (
    create_user,
    login_user,
)

from app.schemas.auth import (
    LoginRequest,
    SignupRequest,
    TokenResponse,
    RefreshTokenRequest,
    AccessTokenResponse,
)

from app.services.auth_service import (
    create_user,
    login_user,
    refresh_access_token,
    logout_user,
)

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
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    return login_user(
        LoginRequest(
            email=form_data.username,
            password=form_data.password,
        ),
        db,
    )


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
    data: RefreshTokenRequest,
):
    return refresh_access_token(data)

@router.post("/logout")
def logout():
    return logout_user()