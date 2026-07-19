from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

# Enum representing the reading status of a book
from app.models.enums import BookStatus


# Request schema for creating a new book
class BookCreate(BaseModel):
    # Book title
    title: str

    # Book author
    author: str

    # Initial reading status
    status: BookStatus = BookStatus.WANT_TO_READ

    # Total number of pages
    total_pages: int | None = None

    # User rating between 1 and 5
    rating: int | None = Field(None, ge=1, le=5)

    # Optional notes about the book
    notes: str | None = None


# Request schema for updating book details
class BookUpdate(BaseModel):
    # Updated book title
    title: str | None = None

    # Updated author name
    author: str | None = None

    # Updated reading status
    status: BookStatus | None = None

    # Updated total pages
    total_pages: int | None = None

    # Updated reading progress
    current_page: int | None = None

    # Updated rating
    rating: int | None = Field(None, ge=1, le=5)

    # Updated notes
    notes: str | None = None


# Request schema for updating reading progress
class ReadingProgressUpdate(BaseModel):
    # Current page reached by the reader
    current_page: int = Field(..., ge=0)


# Response schema for book details
class BookResponse(BaseModel):
    # Unique book ID
    id: int

    # Book title
    title: str

    # Book author
    author: str

    # Current reading status
    status: BookStatus

    # Total number of pages
    total_pages: int | None

    # Current page reached
    current_page: int | None

    # User rating
    rating: int | None

    # Personal notes
    notes: str | None

    # Date when the book was added
    created_at: datetime

    # Date when the book was completed
    finished_at: datetime | None

    # Indicates whether the book is marked as favorite
    is_favorite: bool

    # Enable conversion from SQLAlchemy models
    model_config = ConfigDict(from_attributes=True)