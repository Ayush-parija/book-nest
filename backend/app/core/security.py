from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from pwdlib import PasswordHash

# Application settings
from app.core.config import settings

# Password hashing utility
password_hash = PasswordHash.recommended()

# JWT signing algorithm
ALGORITHM = "HS256"


# Hash a plain text password
def hash_password(password: str) -> str:
    return password_hash.hash(password)


# Verify a password against its hashed value
def verify_password(password: str, hashed_password: str) -> bool:
    return password_hash.verify(password, hashed_password)


# Generate a new access token
def create_access_token(user_id: int) -> str:
    # Set the token expiration time
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes
    )

    # JWT payload
    payload = {
        "sub": str(user_id),
        "type": "access",
        "exp": expire,
    }

    # Create and return the JWT
    return jwt.encode(payload, settings.secret_key, algorithm=ALGORITHM)


# Generate a new refresh token
def create_refresh_token(user_id: int) -> str:
    # Set the token expiration time
    expire = datetime.now(timezone.utc) + timedelta(days=7)

    # JWT payload
    payload = {
        "sub": str(user_id),
        "type": "refresh",
        "exp": expire,
    }

    # Create and return the JWT
    return jwt.encode(payload, settings.secret_key, algorithm=ALGORITHM)


# Decode and validate a JWT token
def decode_token(token: str):
    try:
        # Decode the token using the secret key
        return jwt.decode(
            token,
            settings.secret_key,
            algorithms=[ALGORITHM],
        )

    # Return None if the token is invalid
    except JWTError as e:
        print("JWT ERROR:", str(e))
        return None