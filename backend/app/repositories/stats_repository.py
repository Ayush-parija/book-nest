from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.book import Book
from app.models.enums import BookStatus


class StatsRepository:

    @staticmethod
    def get_stats(
        db: Session,
        owner_id: int,
    ):
        total_books = (
            db.query(func.count(Book.id))
            .filter(Book.owner_id == owner_id)
            .scalar()
        ) or 0

        want_to_read = (
            db.query(func.count(Book.id))
            .filter(
                Book.owner_id == owner_id,
                Book.status == BookStatus.WANT_TO_READ,
            )
            .scalar()
        ) or 0

        reading = (
            db.query(func.count(Book.id))
            .filter(
                Book.owner_id == owner_id,
                Book.status == BookStatus.READING,
            )
            .scalar()
        ) or 0

        finished = (
            db.query(func.count(Book.id))
            .filter(
                Book.owner_id == owner_id,
                Book.status == BookStatus.FINISHED,
            )
            .scalar()
        ) or 0

        total_pages_read = (
            db.query(func.sum(Book.current_page))
            .filter(Book.owner_id == owner_id)
            .scalar()
        ) or 0

        average_rating = (
            db.query(func.avg(Book.rating))
            .filter(
                Book.owner_id == owner_id,
                Book.rating.isnot(None),
            )
            .scalar()
        ) or 0

        return {
            "total_books": total_books,
            "want_to_read": want_to_read,
            "reading": reading,
            "finished": finished,
            "total_pages_read": total_pages_read,
            "average_rating": round(float(average_rating), 2),
        }