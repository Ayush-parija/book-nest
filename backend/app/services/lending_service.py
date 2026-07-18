from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User

from app.repositories.book_repository import BookRepository
from app.repositories.lending_repository import LendingRepository
from app.repositories.user_repository import UserRepository

from app.schemas.lending import LendBookRequest

from app.services.activity_service import log_activity


# ----------------------------------------
# Lend Book
# ----------------------------------------

def lend_book(
    db: Session,
    current_user: User,
    book_id: int,
    data: LendBookRequest,
):
    # Find book
    book = BookRepository.get_by_id(
        db=db,
        book_id=book_id,
        owner_id=current_user.id,
    )

    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found.",
        )

    # Find borrower
    borrower = UserRepository.get_by_email(
        data.email,
        db,
    )

    if borrower is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Borrower not found.",
        )

    # Cannot lend to yourself
    if borrower.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot lend a book to yourself.",
        )

    # Check active lending
    active = LendingRepository.get_active_lending(
        db=db,
        book_id=book.id,
    )

    if active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Book is already lent.",
        )

    lending = LendingRepository.create(
        db=db,
        book=book,
        borrower_id=borrower.id,
    )

    log_activity(
        db=db,
        current_user=current_user,
        action="BOOK_LENT",
        message=f"{current_user.name} lent '{book.title}' to {borrower.name}",
    )

    return lending


# ----------------------------------------
# Return Book
# ----------------------------------------

def return_book(
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
            detail="Book not found.",
        )

    lending = LendingRepository.get_active_lending(
        db=db,
        book_id=book.id,
    )

    if lending is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Book is not currently lent.",
        )

    LendingRepository.return_book(
        db=db,
        lending=lending,
    )

    log_activity(
        db=db,
        current_user=current_user,
        action="BOOK_RETURNED",
        message=f"{current_user.name} returned '{book.title}'",
    )

    return {
        "message": "Book returned successfully."
    }


# ----------------------------------------
# Borrowed Books
# ----------------------------------------

def get_borrowed_books(
    db: Session,
    current_user: User,
):
    lendings = LendingRepository.get_borrowed_books(
        db=db,
        borrower_id=current_user.id,
    )

    result = []

    for lending in lendings:
        result.append({
            "lending_id": lending.id,
            "book_id": lending.book.id,
            "title": lending.book.title,
            "author": lending.book.author,
            "owner_name": lending.owner.name,
            "lent_at": lending.lent_at,
        })

    return result


# ----------------------------------------
# Lent Books
# ----------------------------------------

def get_lent_books(
    db: Session,
    current_user: User,
):
    lendings = LendingRepository.get_lent_books(
        db=db,
        owner_id=current_user.id,
    )

    result = []

    for lending in lendings:
        result.append({
            "id": lending.id,
            "book_id": lending.book.id,
            "book_title": lending.book.title,
            "borrower_email": lending.borrower.email,
            "owner_email": lending.owner.email,
            "lent_at": lending.lent_at,
            "returned_at": lending.returned_at,
        })

    return result