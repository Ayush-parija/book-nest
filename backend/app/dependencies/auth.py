from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

# Security utilities
from app.core.security import decode_token

# Database dependency
from app.dependencies.database import get_db

# User database model
from app.models.user import User

# User repository
from app.repositories.user_repository import UserRepository

# OAuth2 authentication scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# Retrieve the currently authenticated user
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:

    # Display the received token for debugging
    print("TOKEN:", token)

    # Decode the JWT token
    payload = decode_token(token)
    print("PAYLOAD:", payload)

    # Reject the request if the token is invalid
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    # Display token information for debugging
    print("TYPE:", payload.get("type"))
    print("SUB:", payload.get("sub"))

    # Retrieve the user from the database
    user = UserRepository.get_by_id(int(payload["sub"]), db)

    # Display the retrieved user for debugging
    print("USER:", user)

    # Reject the request if the user does not exist
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    # Return the authenticated user
    return user