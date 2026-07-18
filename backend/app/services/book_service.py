# =========================================================
# File: book_service.py
# Purpose:
# Handles all business logic related to book management.
#
# Responsibilities:
# - Create, Read, Update, and Delete (CRUD) operations for books
# - Manage reading progress updates
# - Toggle book favorite status
# - Integrate with activity logging for book-related actions
#
# Depends on:
# - BookRepository
# - ActivityService
# - User model
#
# Used by:
# - book.py router
# - other services needing book validation (e.g., lending_service.py)
# =========================================================

# Navigation
# [1] Third-party Libraries
# [2] Local Models & Schemas
# [3] Repositories
# [4] Cross-Service Dependencies
# [5] Book CRUD Operations
# [6] Reading Progress
# [7] Favorite Operations

# =====================================================
# [1] Third-party Libraries
# =====================================================
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import asyncio

# =====================================================
# [2] Local Models & Schemas
# =====================================================
from app.models.user import User
from app.models.enums import BookStatus
from app.schemas.book import (
    BookCreate,
    BookUpdate,
    ReadingProgressUpdate,
)

# =====================================================
# [3] Repositories
# =====================================================
from app.repositories.book_repository import BookRepository

# =====================================================
# [4] Cross-Service Dependencies
# =====================================================
from app.services.activity_service import log_activity
from app.websocket.connection_manager import manager


# =====================================================
# [5] Book CRUD Operations
# =====================================================

def create_book(
    db: Session,
    current_user: User,
    data: BookCreate,
):
    """
    ---------------------------------------------------------
    Function:
    create_book()

    Purpose:
    Creates a new book owned by the authenticated user.

    Parameters:
    db: Database session
    current_user: The authenticated User instance
    data: BookCreate schema containing book details

    Returns:
    Book: The newly created Book database model

    Raises:
    None

    Side Effects:
    - Inserts a record into the books table
    - Creates an activity log entry
    ---------------------------------------------------------
    """
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


def get_book(
    db: Session,
    current_user: User,
    book_id: int,
):
    """
    ---------------------------------------------------------
    Function:
    get_book()

    Purpose:
    Retrieves a specific book belonging to the current user.

    Parameters:
    db: Database session
    current_user: The authenticated User instance
    book_id: Integer ID of the book

    Returns:
    Book: The retrieved Book database model

    Raises:
    404 HTTPException: If the book does not exist or does not belong to the user

    Side Effects:
    None
    ---------------------------------------------------------
    """
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
    """
    ---------------------------------------------------------
    Function:
    get_books()

    Purpose:
    Retrieves a paginated, filtered, and sorted list of the user's books.

    Parameters:
    db: Database session
    current_user: The authenticated User instance
    page, page_size: Pagination parameters
    status, search, sort_by, order: Filtering and sorting parameters

    Returns:
    list[Book]: A list of Book database models

    Raises:
    None

    Side Effects:
    None
    ---------------------------------------------------------
    """
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


def update_book(
    db: Session,
    current_user: User,
    book_id: int,
    data: BookUpdate,
):
    """
    ---------------------------------------------------------
    Function:
    update_book()

    Purpose:
    Updates the metadata of a specific book owned by the user.

    Parameters:
    db: Database session
    current_user: The authenticated User instance
    book_id: Integer ID of the book
    data: BookUpdate schema containing updated fields

    Returns:
    Book: The updated Book database model

    Raises:
    404 HTTPException: If the book is not found

    Side Effects:
    - Updates the book record in the database
    - Creates an activity log entry
    ---------------------------------------------------------
    """
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


def delete_book(
    db: Session,
    current_user: User,
    book_id: int,
):
    """
    ---------------------------------------------------------
    Function:
    delete_book()

    Purpose:
    Deletes a specific book owned by the user.

    Parameters:
    db: Database session
    current_user: The authenticated User instance
    book_id: Integer ID of the book

    Returns:
    dict: A success message

    Raises:
    404 HTTPException: If the book is not found

    Side Effects:
    - Deletes the book record from the database
    - Creates an activity log entry
    ---------------------------------------------------------
    """
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


# =====================================================
# [6] Reading Progress
# =====================================================

def update_reading_progress(
    db: Session,
    current_user: User,
    book_id: int,
    data: ReadingProgressUpdate,
):
    """
    ---------------------------------------------------------
    Function:
    update_reading_progress()

    Purpose:
    Updates the current page read for a specific book.

    Parameters:
    db: Database session
    current_user: The authenticated User instance
    book_id: Integer ID of the book
    data: ReadingProgressUpdate schema containing the new current_page

    Returns:
    Book: The updated Book database model

    Raises:
    404 HTTPException: If the book is not found
    400 HTTPException: If the book has no total pages set, or the current page is invalid

    Side Effects:
    - Updates the book record in the database
    - Creates an activity log entry
    ---------------------------------------------------------
    """
    book = get_book(
        db=db,
        current_user=current_user,
        book_id=book_id,
    )

    # Validate reading progress constraints
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


# =====================================================
# [7] Favorite Operations
# =====================================================

def toggle_favorite(
    db: Session,
    current_user: User,
    book_id: int,
):
    """
    ---------------------------------------------------------
    Function:
    toggle_favorite()

    Purpose:
    Toggles the favorite status of a specific book (True -> False -> True).

    Parameters:
    db: Database session
    current_user: The authenticated User instance
    book_id: Integer ID of the book

    Returns:
    Book: The updated Book database model

    Raises:
    404 HTTPException: If the book is not found

    Side Effects:
    - Updates the is_favorite boolean in the database
    - Creates an activity log entry
    ---------------------------------------------------------
    """
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


def get_favorite_books(
    db: Session,
    current_user: User,
):
    """
    ---------------------------------------------------------
    Function:
    get_favorite_books()

    Purpose:
    Retrieves all books marked as favorite by the user.

    Parameters:
    db: Database session
    current_user: The authenticated User instance

    Returns:
    list[Book]: A list of favorite Book database models

    Raises:
    None

    Side Effects:
    None
    ---------------------------------------------------------
    """
    return BookRepository.get_favorites(
        db=db,
        owner_id=current_user.id,
    )