from sqlalchemy.orm import Session

# User database model
from app.models.user import User


# Repository class for handling user-related database operations
class UserRepository:

    # Get a user by email address
    @staticmethod
    def get_by_email(email: str, db: Session) -> User | None:
        return (
            db.query(User)
            .filter(User.email == email)
            .first()
        )

    # Get a user by ID
    @staticmethod
    def get_by_id(user_id: int, db: Session) -> User | None:
        return (
            db.query(User)
            .filter(User.id == user_id)
            .first()
        )

    # Create a new user
    @staticmethod
    def create(user: User, db: Session) -> User:
        # Save the user to the database
        db.add(user)
        db.commit()
        db.refresh(user)

        return user