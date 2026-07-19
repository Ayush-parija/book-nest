from pydantic_settings import BaseSettings, SettingsConfigDict


# Application configuration loaded from environment variables
class Settings(BaseSettings):
    # Database connection URL
    database_url: str

    # Secret key used for JWT token generation
    secret_key: str

    # Access token expiration time in minutes
    access_token_expire_minutes: int

    # Refresh token expiration time in days
    refresh_token_expire_days: int

    # Load configuration from the .env file
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


# Create a global settings instance
settings = Settings()