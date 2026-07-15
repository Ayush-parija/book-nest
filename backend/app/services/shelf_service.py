from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User

from app.repositories.book_repository import BookRepository
from app.repositories.shelf_repository import ShelfRepository

from app.schemas.shelf import ShelfCreate, ShelfUpdate


def create_shelf(
    db: Session,
    current_user: User,
    data: ShelfCreate,
):
    return ShelfRepository.create(
        db=db,
        owner_id=current_user.id,
        data=data,
    )


def get_shelves(
    db: Session,
    current_user: User,
):
    return ShelfRepository.get_all(
        db=db,
        owner_id=current_user.id,
    )


def get_shelf(
    db: Session,
    current_user: User,
    shelf_id: int,
):
    shelf = ShelfRepository.get_by_id(
        db,
        shelf_id,
        current_user.id,
    )

    if not shelf:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shelf not found",
        )

    return shelf


def update_shelf(
    db: Session,
    current_user: User,
    shelf_id: int,
    data: ShelfUpdate,
):
    shelf = get_shelf(
        db,
        current_user,
        shelf_id,
    )

    return ShelfRepository.update(
        db,
        shelf,
        data,
    )


def delete_shelf(
    db: Session,
    current_user: User,
    shelf_id: int,
):
    shelf = get_shelf(
        db,
        current_user,
        shelf_id,
    )

    ShelfRepository.delete(
        db,
        shelf,
    )

    return {
        "message": "Shelf deleted successfully"
    }


# -------------------------
# Book ↔ Shelf
# -------------------------

def add_book_to_shelf(
    db: Session,
    current_user: User,
    shelf_id: int,
    book_id: int,
):
    shelf = get_shelf(
        db,
        current_user,
        shelf_id,
    )

    book = BookRepository.get_by_id(
        db,
        book_id,
        current_user.id,
    )

    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found",
        )

    return ShelfRepository.add_book(
        db,
        shelf,
        book,
    )


def remove_book_from_shelf(
    db: Session,
    current_user: User,
    shelf_id: int,
    book_id: int,
):
    shelf = get_shelf(
        db,
        current_user,
        shelf_id,
    )

    book = BookRepository.get_by_id(
        db,
        book_id,
        current_user.id,
    )

    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found",
        )

    return ShelfRepository.remove_book(
        db,
        shelf,
        book,
    )


def list_books_in_shelf(
    db: Session,
    current_user: User,
    shelf_id: int,
):
    shelf = get_shelf(
        db,
        current_user,
        shelf_id,
    )

    return ShelfRepository.list_books(shelf)