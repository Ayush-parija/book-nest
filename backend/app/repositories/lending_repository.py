from datetime import datetime

from sqlalchemy.orm import Session

from app.models.book import Book
from app.models.lending import Lending


class LendingRepository:

    # -------------------------
    # Create Lending
    # -------------------------

    @staticmethod
    def create(
        db: Session,
        book: Book,
        borrower_id: int,
    ):
        lending = Lending(
            book_id=book.id,
            owner_id=book.owner_id,
            borrower_id=borrower_id,
        )

        db.add(lending)
        db.commit()
        db.refresh(lending)

        return lending

    # -------------------------
    # Get Active Lending
    # -------------------------

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

    @staticmethod
    def return_book(
        db: Session,
        lending: Lending,
    ):
        lending.returned_at = datetime.utcnow()

        db.commit()
        db.refresh(lending)

        return lending

    # -------------------------
    # Borrowed Books
    # -------------------------

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