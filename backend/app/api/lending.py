from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

# Database session dependency
from app.db.dependencies import get_db

# Dependency to get the currently authenticated user
from app.dependencies.auth import get_current_user
from app.models.user import User

# Request and response schemas for lending operations
from app.schemas.lending import (
    LendBookRequest,
    LendingResponse,
    ReturnBookResponse,
)

# Service functions that handle lending business logic
from app.services.lending_service import (
    lend_book,
    return_book,
    get_borrowed_books,
    get_lent_books,
)

# Router for all lending-related endpoints
router = APIRouter(
    prefix="/lending",
    tags=["Lending"],
)


# Get the list of books borrowed by the current user
@router.get("/borrowed")
def borrowed_books(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_borrowed_books(
        db=db,
        current_user=current_user,
    )


# Get the list of books the current user has lent to others
@router.get("/lent")
def lent_books(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_lent_books(
        db=db,
        current_user=current_user,
    )


# Lend a book to another user
@router.post(
    "/books/{book_id}/lend",
    response_model=LendingResponse,
)
def lend(
    book_id: int,
    data: LendBookRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return lend_book(
        db=db,
        current_user=current_user,
        book_id=book_id,
        data=data,
    )


# Mark a previously lent book as returned
@router.post(
    "/books/{book_id}/return",
    response_model=ReturnBookResponse,
)
def return_lent_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return return_book(
        db=db,
        current_user=current_user,
        book_id=book_id,
    )