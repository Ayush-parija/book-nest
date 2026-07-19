from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import Session

# Database models
from app.models.book import Book
from app.models.enums import BookStatus
from app.models.shelf import Shelf
from app.models.user import User


# Repository class for dashboard-related database operations
class DashboardRepository:

    # Get a user by ID
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

    # Get recently added books
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

    # Get favorite books of the user
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

    # Get books that are currently being read
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

    # Get all shelves owned by the user
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

    # Calculate dashboard statistics
    @staticmethod
    def get_statistics(
        db: Session,
        owner_id: int,
    ):
        # Fetch all books belonging to the user
        books = (
            db.query(Book)
            .filter(Book.owner_id == owner_id)
            .all()
        )

        # Total number of books
        total_books = len(books)

        # Count books in "Want to Read" status
        want_to_read = sum(
            1 for book in books
            if book.status == BookStatus.WANT_TO_READ
        )

        # Count books currently being read
        reading = sum(
            1 for book in books
            if book.status == BookStatus.READING
        )

        # Count finished books
        finished = sum(
            1 for book in books
            if book.status == BookStatus.FINISHED
        )

        # Current year for yearly statistics
        current_year = datetime.utcnow().year

        # Count books finished in the current year
        finished_this_year = sum(
            1 for book in books
            if book.status == BookStatus.FINISHED and book.finished_at and book.finished_at.year == current_year
        )

        # Calculate total pages read
        total_pages_read = sum(
            book.current_page or 0
            for book in books
        )

        # Collect all available ratings
        ratings = [
            book.rating
            for book in books
            if book.rating is not None
        ]

        # Calculate average rating
        average_rating = (
            round(sum(ratings) / len(ratings), 2)
            if ratings
            else 0
        )

        # Find the shelf with the highest number of books
        shelves = db.query(Shelf).filter(Shelf.owner_id == owner_id).all()
        largest_shelf = None
        max_books = -1

        for shelf in shelves:
            if len(shelf.books) > max_books:
                max_books = len(shelf.books)
                largest_shelf = shelf.name

        # Default value when no shelves exist
        if not shelves:
            largest_shelf = "No shelves"

        # Return all dashboard statistics
        return {
            "total_books": total_books,
            "want_to_read": want_to_read,
            "reading": reading,
            "finished": finished,
            "finished_this_year": finished_this_year,
            "total_pages_read": total_pages_read,
            "average_rating": average_rating,
            "largest_shelf": largest_shelf,
        }