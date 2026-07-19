from datetime import datetime

from sqlalchemy import asc, desc, or_
from sqlalchemy.orm import Session

# Book database model
from app.models.book import Book

# Enum for book reading status
from app.models.enums import BookStatus

# Request schemas for creating and updating books
from app.schemas.book import BookCreate, BookUpdate


# Repository class that handles all book database operations
class BookRepository:

    # Create a new book
    @staticmethod
    def create(
        db: Session,
        owner_id: int,
        data: BookCreate,
    ) -> Book:
        # Create a new Book object
        book = Book(
            owner_id=owner_id,
            title=data.title,
            author=data.author,
            status=data.status,
            total_pages=data.total_pages,
            rating=data.rating,
            notes=data.notes,
        )

        # Save the book to the database
        db.add(book)
        db.commit()
        db.refresh(book)

        return book

    # Get a book by its ID for a specific owner
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

    # Get a book by its ID without checking the owner
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

    # Retrieve books with pagination, filtering, searching, and sorting
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
        # Start with books owned by the current user
        query = db.query(Book).filter(
            Book.owner_id == owner_id
        )

        # Apply status filter if provided
        if status:
            query = query.filter(
                Book.status == status
            )

        # Search by title or author
        if search:
            query = query.filter(
                or_(
                    Book.title.ilike(f"%{search}%"),
                    Book.author.ilike(f"%{search}%"),
                )
            )

        # Available sorting options
        sort_columns = {
            "title": Book.title,
            "rating": Book.rating,
            "created_at": Book.created_at,
        }

        # Use created_at as the default sorting column
        column = sort_columns.get(
            sort_by,
            Book.created_at,
        )

        # Apply sorting order
        if order == "asc":
            query = query.order_by(
                asc(column)
            )
        else:
            query = query.order_by(
                desc(column)
            )

        # Return paginated results
        return (
            query
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )

    # Update book details
    @staticmethod
    def update(
        db: Session,
        book: Book,
        data: BookUpdate,
    ):
        # Get only the fields provided in the request
        update_data = data.model_dump(
            exclude_unset=True
        )

        # Update each field dynamically
        for key, value in update_data.items():
            setattr(book, key, value)

        db.commit()
        db.refresh(book)

        return book

    # Update the reading progress of a book
    @staticmethod
    def update_progress(
        db: Session,
        book: Book,
        current_page: int,
    ):
        # Update the current page
        book.current_page = current_page

        # Update book status based on reading progress
        if book.total_pages:

            # Mark as finished when all pages are completed
            if current_page >= book.total_pages:
                book.current_page = book.total_pages
                book.status = BookStatus.FINISHED
                book.finished_at = datetime.utcnow()

            # Mark as currently reading
            elif current_page > 0:
                book.status = BookStatus.READING
                book.finished_at = None

            # Reset to want-to-read if no pages have been read
            else:
                book.status = BookStatus.WANT_TO_READ
                book.finished_at = None

        db.commit()
        db.refresh(book)

        return book

    # Delete a book from the database
    @staticmethod
    def delete(
        db: Session,
        book: Book,
    ):
        db.delete(book)
        db.commit()

    # Add or remove a book from favorites
    @staticmethod
    def toggle_favorite(
        db: Session,
        book: Book,
        ):
        # Switch the favorite status
        book.is_favorite = not book.is_favorite

        db.commit()
        db.refresh(book)

        return book

    # Get all favorite books of a user
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