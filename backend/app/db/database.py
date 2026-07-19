from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker

# Application configuration
from app.core.config import settings


# Create the SQLAlchemy database engine
engine = create_engine(
    settings.database_url,
    echo=True,
)


# Create a session factory for database operations
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


# Base class for all SQLAlchemy models
class Base(DeclarativeBase):
    pass