from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

# Application settings
from app.core.config import settings

# Database dependency
from app.dependencies.database import get_db

# User database model
from app.models.user import User

# OAuth2 authentication scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# JWT signing algorithm
ALGORITHM = "HS256"


# Get the currently authenticated user
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    # Exception raised when authentication fails
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decode the JWT access token
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[ALGORITHM],
        )

        # Extract the user ID from the token payload
        user_id = payload.get("sub")

        # Reject the request if the user ID is missing
        if user_id is None:
            raise credentials_exception

    # Handle invalid or expired tokens
    except JWTError:
        raise credentials_exception

    # Retrieve the user from the database
    user = db.get(User, int(user_id))

    # Reject the request if the user does not exist
    if user is None:
        raise credentials_exception

    # Return the authenticated user
    return user