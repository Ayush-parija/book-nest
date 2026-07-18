from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.enums import BookStatus

from app.repositories.book_repository import BookRepository

from app.schemas.book import (
    BookCreate,
    BookUpdate,
    ReadingProgressUpdate,
)

from app.services.activity_service import log_activity

from app.websocket.connection_manager import manager
import asyncio


# -------------------------
# Create Book
# -------------------------

def create_book(
    db: Session,
    current_user: User,
    data: BookCreate,
):
    book = BookRepository.create(
        db=db,
        owner_id=current_user.id,
        data=data,
    )

    log_activity(
        db=db,
        current_user=current_user,
        action="BOOK_CREATED",
        message=f"{current_user.name} created '{book.title}'",
    )

    return book


# -------------------------
# Get Single Book
# -------------------------

def get_book(
    db: Session,
    current_user: User,
    book_id: int,
):
    book = BookRepository.get_by_id(
        db=db,
        book_id=book_id,
        owner_id=current_user.id,
    )

    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found",
        )

    return book


# -------------------------
# Get All Books
# -------------------------

def get_books(
    db: Session,
    current_user: User,
    page: int = 1,
    page_size: int = 10,
    status: BookStatus | None = None,
    search: str | None = None,
    sort_by: str = "created_at",
    order: str = "desc",
):
    return BookRepository.get_all(
        db=db,
        owner_id=current_user.id,
        page=page,
        page_size=page_size,
        status=status,
        search=search,
        sort_by=sort_by,
        order=order,
    )


# -------------------------
# Update Book
# -------------------------

def update_book(
    db: Session,
    current_user: User,
    book_id: int,
    data: BookUpdate,
):
    book = get_book(
        db=db,
        current_user=current_user,
        book_id=book_id,
    )

    updated_book = BookRepository.update(
        db=db,
        book=book,
        data=data,
    )

    log_activity(
        db=db,
        current_user=current_user,
        action="BOOK_UPDATED",
        message=f"{current_user.name} updated '{updated_book.title}'",
    )

    return updated_book


# -------------------------
# Delete Book
# -------------------------

def delete_book(
    db: Session,
    current_user: User,
    book_id: int,
):
    book = get_book(
        db=db,
        current_user=current_user,
        book_id=book_id,
    )

    title = book.title

    BookRepository.delete(
        db=db,
        book=book,
    )

    log_activity(
        db=db,
        current_user=current_user,
        action="BOOK_DELETED",
        message=f"{current_user.name} deleted '{title}'",
    )

    return {
        "message": "Book deleted successfully"
    }


# -------------------------
# Reading Progress
# -------------------------

def update_reading_progress(
    db: Session,
    current_user: User,
    book_id: int,
    data: ReadingProgressUpdate,
):
    book = get_book(
        db=db,
        current_user=current_user,
        book_id=book_id,
    )

    if book.total_pages is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Book does not have total pages.",
        )

    if data.current_page < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current page cannot be negative.",
        )

    if data.current_page > book.total_pages:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current page cannot exceed total pages.",
        )

    updated_book = BookRepository.update_progress(
        db=db,
        book=book,
        current_page=data.current_page,
    )

    log_activity(
        db=db,
        current_user=current_user,
        action="READING_PROGRESS_UPDATED",
        message=f"{current_user.name} updated reading progress for '{updated_book.title}' to page {updated_book.current_page}",
    )

    return updated_book


# -------------------------
# Toggle Favorite
# -------------------------

def toggle_favorite(
    db: Session,
    current_user: User,
    book_id: int,
):
    book = get_book(
        db=db,
        current_user=current_user,
        book_id=book_id,
    )

    updated_book = BookRepository.toggle_favorite(
        db=db,
        book=book,
    )

    action = (
        "FAVORITE_ADDED"
        if updated_book.is_favorite
        else "FAVORITE_REMOVED"
    )

    message = (
        f"{current_user.name} added '{updated_book.title}' to favorites"
        if updated_book.is_favorite
        else f"{current_user.name} removed '{updated_book.title}' from favorites"
    )

    log_activity(
        db=db,
        current_user=current_user,
        action=action,
        message=message,
    )

    return updated_book


# -------------------------
# Get Favorite Books
# -------------------------

def get_favorite_books(
    db: Session,
    current_user: User,
):
    return BookRepository.get_favorites(
        db=db,
        owner_id=current_user.id,
    )