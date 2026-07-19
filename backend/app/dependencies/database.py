from collections.abc import Generator

from sqlalchemy.orm import Session

# Database session factory
from app.db.database import SessionLocal


# Create and manage a database session for each request
def get_db() -> Generator[Session, None, None]:
    # Create a new database session
    db = SessionLocal()

    try:
        # Provide the session to the requesting function
        yield db
    finally:
        # Always close the session after use
        db.close()