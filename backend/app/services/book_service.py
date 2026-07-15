from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.enums import BookStatus
from app.repositories.book_repository import BookRepository
from app.schemas.book import BookCreate, BookUpdate


def create_book(
    db: Session,
    current_user: User,
    data: BookCreate,
):
    return BookRepository.create(
        db=db,
        owner_id=current_user.id,
        data=data,
    )


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


def update_book(
    db: Session,
    current_user: User,
    book_id: int,
    data: BookUpdate,
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

    return BookRepository.update(
        db=db,
        book=book,
        data=data,
    )


def delete_book(
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

    BookRepository.delete(
        db=db,
        book=book,
    )

    return {
        "message": "Book deleted successfully"
    }