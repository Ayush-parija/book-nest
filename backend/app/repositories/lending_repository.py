from datetime import datetime

from sqlalchemy.orm import Session

# Database models
from app.models.book import Book
from app.models.lending import Lending


# Repository class for handling lending-related database operations
class LendingRepository:

    # -------------------------
    # Create Lending
    # -------------------------

    # Create a new lending record for a book
    @staticmethod
    def create(
        db: Session,
        book: Book,
        borrower_id: int,
    ):
        # Create a new Lending object
        lending = Lending(
            book_id=book.id,
            owner_id=book.owner_id,
            borrower_id=borrower_id,
        )

        # Save the lending record
        db.add(lending)
        db.commit()
        db.refresh(lending)

        return lending

    # -------------------------
    # Get Active Lending
    # -------------------------

    # Retrieve the active lending record for a specific book
    @staticmethod
    def get_active_lending(
        db: Session,
        book_id: int,
    ):
        return (
            db.query(Lending)
            .filter(
                Lending.book_id == book_id,
                Lending.returned_at.is_(None),
            )
            .first()
        )

    # -------------------------
    # Return Book
    # -------------------------

    # Mark a borrowed book as returned
    @staticmethod
    def return_book(
        db: Session,
        lending: Lending,
    ):
        # Store the return date and time
        lending.returned_at = datetime.utcnow()

        db.commit()
        db.refresh(lending)

        return lending

    # -------------------------
    # Borrowed Books
    # -------------------------

    # Get all books currently borrowed by a user
    @staticmethod
    def get_borrowed_books(
        db: Session,
        borrower_id: int,
    ):
        return (
            db.query(Lending)
            .filter(
                Lending.borrower_id == borrower_id,
                Lending.returned_at.is_(None),
            )
            .all()
        )

    # -------------------------
    # Lent Books
    # -------------------------

    # Get all books currently lent by a user
    @staticmethod
    def get_lent_books(
        db: Session,
        owner_id: int,
    ):
        return (
            db.query(Lending)
            .filter(
                Lending.owner_id == owner_id,
                Lending.returned_at.is_(None),
            )
            .all()
        )