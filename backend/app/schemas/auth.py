from pydantic import BaseModel, EmailStr, Field


# Request schema for user registration
class SignupRequest(BaseModel):
    # User's full name
    name: str = Field(min_length=2, max_length=100)

    # User's email address
    email: EmailStr

    # User's password
    password: str = Field(min_length=8)


# Request schema for user login
class LoginRequest(BaseModel):
    # Registered email address
    email: EmailStr

    # User password
    password: str


# Request schema for refreshing an access token
class RefreshTokenRequest(BaseModel):
    # Refresh token issued during login
    refresh_token: str


# Response schema containing authentication tokens
class TokenResponse(BaseModel):
    # JWT access token
    access_token: str

    # JWT refresh token
    refresh_token: str

    # Authentication token type
    token_type: str = "bearer"


# Response schema for returning a new access token
class AccessTokenResponse(BaseModel):
    # Newly generated access token
    access_token: str

    # Authentication token type
    token_type: str = "bearer"