from datetime import datetime

from sqlalchemy import asc, desc, or_
from sqlalchemy.orm import Session

from app.models.book import Book
from app.models.enums import BookStatus
from app.schemas.book import BookCreate, BookUpdate


class BookRepository:

    @staticmethod
    def create(
        db: Session,
        owner_id: int,
        data: BookCreate,
    ) -> Book:
        book = Book(
            owner_id=owner_id,
            title=data.title,
            author=data.author,
            status=data.status,
            total_pages=data.total_pages,
            rating=data.rating,
            notes=data.notes,
        )

        db.add(book)
        db.commit()
        db.refresh(book)

        return book

    @staticmethod
    def get_by_id(
        db: Session,
        book_id: int,
        owner_id: int,
    ):
        return (
            db.query(Book)
            .filter(
                Book.id == book_id,
                Book.owner_id == owner_id,
            )
            .first()
        )

    @staticmethod
    def get_by_id_any(
        db: Session,
        book_id: int,
    ):
        return (
            db.query(Book)
            .filter(Book.id == book_id)
            .first()
        )

    @staticmethod
    def get_all(
        db: Session,
        owner_id: int,
        page: int,
        page_size: int,
        status: BookStatus | None,
        search: str | None,
        sort_by: str,
        order: str,
    ):
        query = db.query(Book).filter(
            Book.owner_id == owner_id
        )

        if status:
            query = query.filter(
                Book.status == status
            )

        if search:
            query = query.filter(
                or_(
                    Book.title.ilike(f"%{search}%"),
                    Book.author.ilike(f"%{search}%"),
                )
            )

        sort_columns = {
            "title": Book.title,
            "rating": Book.rating,
            "created_at": Book.created_at,
        }

        column = sort_columns.get(
            sort_by,
            Book.created_at,
        )

        if order == "asc":
            query = query.order_by(
                asc(column)
            )
        else:
            query = query.order_by(
                desc(column)
            )

        return (
            query
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )

    @staticmethod
    def update(
        db: Session,
        book: Book,
        data: BookUpdate,
    ):
        update_data = data.model_dump(
            exclude_unset=True
        )

        for key, value in update_data.items():
            setattr(book, key, value)

        db.commit()
        db.refresh(book)

        return book

    @staticmethod
    def update_progress(
        db: Session,
        book: Book,
        current_page: int,
    ):
        book.current_page = current_page

        if book.total_pages:

            if current_page >= book.total_pages:
                book.current_page = book.total_pages
                book.status = BookStatus.FINISHED
                book.finished_at = datetime.utcnow()

            elif current_page > 0:
                book.status = BookStatus.READING
                book.finished_at = None

            else:
                book.status = BookStatus.WANT_TO_READ
                book.finished_at = None

        db.commit()
        db.refresh(book)

        return book

    @staticmethod
    def delete(
        db: Session,
        book: Book,
    ):
        db.delete(book)
        db.commit()

    @staticmethod
    def toggle_favorite(
        db: Session,
        book: Book,
        ):
        book.is_favorite = not book.is_favorite

        db.commit()
        db.refresh(book)

        return book
    
    @staticmethod
    def get_favorites(
        db: Session,
        owner_id: int,
    ):
        return (
            db.query(Book)
            .filter(
                Book.owner_id == owner_id,
                Book.is_favorite == True,
            )
            .all()
        )