from sqlalchemy import func
from sqlalchemy.orm import Session

# Database models
from app.models.book import Book
from app.models.enums import BookStatus


# Repository class for retrieving book statistics
class StatsRepository:

    # Get reading statistics for a specific user
    @staticmethod
    def get_stats(
        db: Session,
        owner_id: int,
    ):
        # Count the total number of books
        total_books = (
            db.query(func.count(Book.id))
            .filter(Book.owner_id == owner_id)
            .scalar()
        ) or 0

        # Count books marked as "Want to Read"
        want_to_read = (
            db.query(func.count(Book.id))
            .filter(
                Book.owner_id == owner_id,
                Book.status == BookStatus.WANT_TO_READ,
            )
            .scalar()
        ) or 0

        # Count books currently being read
        reading = (
            db.query(func.count(Book.id))
            .filter(
                Book.owner_id == owner_id,
                Book.status == BookStatus.READING,
            )
            .scalar()
        ) or 0

        # Count completed books
        finished = (
            db.query(func.count(Book.id))
            .filter(
                Book.owner_id == owner_id,
                Book.status == BookStatus.FINISHED,
            )
            .scalar()
        ) or 0

        # Calculate the total number of pages read
        total_pages_read = (
            db.query(func.sum(Book.current_page))
            .filter(Book.owner_id == owner_id)
            .scalar()
        ) or 0

        # Calculate the average rating of rated books
        average_rating = (
            db.query(func.avg(Book.rating))
            .filter(
                Book.owner_id == owner_id,
                Book.rating.isnot(None),
            )
            .scalar()
        ) or 0

        # Return all calculated statistics
        return {
            "total_books": total_books,
            "want_to_read": want_to_read,
            "reading": reading,
            "finished": finished,
            "total_pages_read": total_pages_read,
            "average_rating": round(float(average_rating), 2),
        }