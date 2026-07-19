from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

# Database session dependency
from app.db.dependencies import get_db

# Dependency to get the currently logged-in user
from app.dependencies.auth import get_current_user

# Book status enum
from app.models.enums import BookStatus
from app.models.user import User

# Request and response schemas
from app.schemas.book import (
    BookCreate,
    BookUpdate,
    BookResponse,
    ReadingProgressUpdate,
)

# Business logic for book operations
from app.services.book_service import (
    create_book,
    get_book,
    get_books,
    update_book,
    delete_book,
    update_reading_progress,
    toggle_favorite,
    get_favorite_books,
)

# Router for all book-related APIs
router = APIRouter(
    prefix="/books",
    tags=["Books"],
)


# =====================================================
# BOOK CRUD
# =====================================================

# Create a new book for the logged-in user
@router.post("")
def create_new_book(
    data: BookCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_book(
        db=db,
        current_user=current_user,
        data=data,
    )


# Get all books with pagination, filtering, searching and sorting
@router.get(
    "",
    response_model=list[BookResponse],
)
def list_books(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    status: BookStatus | None = None,
    search: str | None = None,
    sort_by: str = "created_at",
    order: str = "desc",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_books(
        db=db,
        current_user=current_user,
        page=page,
        page_size=page_size,
        status=status,
        search=search,
        sort_by=sort_by,
        order=order,
    )


# Return only the user's favorite books
@router.get(
    "/favorites",
    response_model=list[BookResponse],
)
def favorite_books(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_favorite_books(
        db=db,
        current_user=current_user,
    )


# =====================================================
# BOOK CRUD BY ID
# =====================================================

# Get details of a specific book
@router.get(
    "/{book_id}",
    response_model=BookResponse,
)
def get_single_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_book(
        db=db,
        current_user=current_user,
        book_id=book_id,
    )


# Update the details of an existing book
@router.patch(
    "/{book_id}",
    response_model=BookResponse,
)
def edit_book(
    book_id: int,
    data: BookUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return update_book(
        db=db,
        current_user=current_user,
        book_id=book_id,
        data=data,
    )


# Update the current reading progress of a book
@router.patch(
    "/{book_id}/progress",
    response_model=BookResponse,
)
def update_progress(
    book_id: int,
    data: ReadingProgressUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return update_reading_progress(
        db=db,
        current_user=current_user,
        book_id=book_id,
        data=data,
    )


# Mark or unmark a book as favorite
@router.patch(
    "/{book_id}/favorite",
    response_model=BookResponse,
)
def favorite_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return toggle_favorite(
        db=db,
        current_user=current_user,
        book_id=book_id,
    )


# Delete a book owned by the current user
@router.delete(
    "/{book_id}",
)
def remove_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return delete_book(
        db=db,
        current_user=current_user,
        book_id=book_id,
    )