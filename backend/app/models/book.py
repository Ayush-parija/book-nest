from datetime import datetime
import enum

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

# Base class for all database models
from app.db.database import Base

# Association table for the many-to-many relationship
from app.models.shelf import book_shelves

from sqlalchemy import Boolean


# Enum representing the reading status of a book
class BookStatus(str, enum.Enum):
    WANT_TO_READ = "Want to Read"
    READING = "Reading"
    FINISHED = "Finished"


# Book model
class Book(Base):
    # Database table name
    __tablename__ = "books"

    # Unique identifier for each book
    id: Mapped[int] = mapped_column(primary_key=True)

    # Book title
    title: Mapped[str] = mapped_column(String(255))

    # Book author
    author: Mapped[str] = mapped_column(String(255))

    # Current reading status
    status: Mapped[BookStatus] = mapped_column(
        Enum(BookStatus),
        default=BookStatus.WANT_TO_READ,
    )

    # Total number of pages in the book
    total_pages: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    # Current page reached by the reader
    current_page: Mapped[int | None] = mapped_column(
        Integer,
        default=0,
        nullable=True,
    )

    # User rating for the book
    rating: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    # Personal notes about the book
    notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # Date when the book was added
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    # Date when the book was completed
    finished_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    # Owner of the book
    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
    )

    # Relationship with the User model
    owner: Mapped["User"] = relationship(
        "User",
        back_populates="books",
    )

    # Many-to-many relationship with shelves
    shelves: Mapped[list["Shelf"]] = relationship(
        "Shelf",
        secondary=book_shelves,
        back_populates="books",
    )

    # Indicates whether the book is marked as favorite
    is_favorite: Mapped[bool] = mapped_column(
    Boolean,
    default=False,)