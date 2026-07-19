from collections.abc import Generator

from sqlalchemy.orm import Session

# Database session factory
from app.db.database import SessionLocal


# Create and provide a database session for each request
def get_db() -> Generator[Session, None, None]:
    # Create a new database session
    db = SessionLocal()

    try:
        # Make the session available to the request
        yield db
    finally:
        # Close the session after the request is completed
        db.close()