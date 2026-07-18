from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.book import Book
from app.models.enums import BookStatus
from app.models.shelf import Shelf
from app.models.user import User


class DashboardRepository:

    @staticmethod
    def get_user(
        db: Session,
        user_id: int,
    ):
        return (
            db.query(User)
            .filter(User.id == user_id)
            .first()
        )

    @staticmethod
    def get_recent_books(
        db: Session,
        owner_id: int,
        limit: int = 5,
    ):
        return (
            db.query(Book)
            .filter(Book.owner_id == owner_id)
            .order_by(Book.created_at.desc())
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_favorite_books(
        db: Session,
        owner_id: int,
        limit: int = 5,
    ):
        return (
            db.query(Book)
            .filter(
                Book.owner_id == owner_id,
                Book.is_favorite == True,
            )
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_currently_reading(
        db: Session,
        owner_id: int,
    ):
        return (
            db.query(Book)
            .filter(
                Book.owner_id == owner_id,
                Book.status == BookStatus.READING,
            )
            .all()
        )

    @staticmethod
    def get_shelves(
        db: Session,
        owner_id: int,
    ):
        return (
            db.query(Shelf)
            .filter(Shelf.owner_id == owner_id)
            .all()
        )

    @staticmethod
    def get_statistics(
        db: Session,
        owner_id: int,
    ):
        books = (
            db.query(Book)
            .filter(Book.owner_id == owner_id)
            .all()
        )

        total_books = len(books)

        want_to_read = sum(
            1 for book in books
            if book.status == BookStatus.WANT_TO_READ
        )

        reading = sum(
            1 for book in books
            if book.status == BookStatus.READING
        )

        finished = sum(
            1 for book in books
            if book.status == BookStatus.FINISHED
        )

        total_pages_read = sum(
            book.current_page or 0
            for book in books
        )

        ratings = [
            book.rating
            for book in books
            if book.rating is not None
        ]

        average_rating = (
            round(sum(ratings) / len(ratings), 2)
            if ratings
            else 0
        )

        return {
            "total_books": total_books,
            "want_to_read": want_to_read,
            "reading": reading,
            "finished": finished,
            "total_pages_read": total_pages_read,
            "average_rating": average_rating,
        }