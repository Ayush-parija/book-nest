from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User

from app.repositories.book_repository import BookRepository
from app.repositories.shelf_repository import ShelfRepository

from app.schemas.shelf import ShelfCreate, ShelfUpdate

from app.services.permission_service import PermissionService
from app.services.activity_service import log_activity


# ----------------------------------------
# Create Shelf
# ----------------------------------------

def create_shelf(
    db: Session,
    current_user: User,
    data: ShelfCreate,
):
    shelf = ShelfRepository.create(
        db=db,
        owner_id=current_user.id,
        data=data,
    )

    log_activity(
        db=db,
        current_user=current_user,
        action="SHELF_CREATED",
        message=f"{current_user.name} created shelf '{shelf.name}'",
    )

    return shelf


# ----------------------------------------
# Get Shelves
# ----------------------------------------

def get_shelves(
    db: Session,
    current_user: User,
):
    return ShelfRepository.get_all(
        db=db,
        user_id=current_user.id,
    )


# ----------------------------------------
# Get Shelf
# ----------------------------------------

def get_shelf(
    db: Session,
    current_user: User,
    shelf_id: int,
):
    PermissionService.require_viewer(
        db=db,
        shelf_id=shelf_id,
        user_id=current_user.id,
    )

    shelf = ShelfRepository.get_by_id_without_owner(
        db=db,
        shelf_id=shelf_id,
    )

    if shelf is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shelf not found",
        )

    return shelf


# ----------------------------------------
# Update Shelf
# ----------------------------------------

def update_shelf(
    db: Session,
    current_user: User,
    shelf_id: int,
    data: ShelfUpdate,
):
    PermissionService.require_owner(
        db=db,
        shelf_id=shelf_id,
        user_id=current_user.id,
    )

    shelf = ShelfRepository.get_by_id_without_owner(
        db=db,
        shelf_id=shelf_id,
    )

    updated_shelf = ShelfRepository.update(
        db=db,
        shelf=shelf,
        data=data,
    )

    log_activity(
        db=db,
        current_user=current_user,
        action="SHELF_UPDATED",
        message=f"{current_user.name} updated shelf '{updated_shelf.name}'",
    )

    return updated_shelf


# ----------------------------------------
# Delete Shelf
# ----------------------------------------

def delete_shelf(
    db: Session,
    current_user: User,
    shelf_id: int,
):
    PermissionService.require_owner(
        db=db,
        shelf_id=shelf_id,
        user_id=current_user.id,
    )

    shelf = ShelfRepository.get_by_id_without_owner(
        db=db,
        shelf_id=shelf_id,
    )

    shelf_name = shelf.name

    ShelfRepository.delete(
        db=db,
        shelf=shelf,
    )

    log_activity(
        db=db,
        current_user=current_user,
        action="SHELF_DELETED",
        message=f"{current_user.name} deleted shelf '{shelf_name}'",
    )

    return {
        "message": "Shelf deleted successfully"
    }


# ----------------------------------------
# Add Book to Shelf
# ----------------------------------------

def add_book_to_shelf(
    db: Session,
    current_user: User,
    shelf_id: int,
    book_id: int,
):
    PermissionService.require_editor(
        db=db,
        shelf_id=shelf_id,
        user_id=current_user.id,
    )

    shelf = ShelfRepository.get_by_id_without_owner(
        db=db,
        shelf_id=shelf_id,
    )

    book = BookRepository.get_by_id(
        db=db,
        book_id=book_id,
        owner_id=current_user.id,
    )

    if not book:
        raise HTTPException(
            status_code=404,
            detail="Book not found",
        )

    ShelfRepository.add_book(
        db=db,
        shelf=shelf,
        book=book,
    )

    log_activity(
        db=db,
        current_user=current_user,
        action="BOOK_ADDED_TO_SHELF",
        message=f"{current_user.name} added '{book.title}' to shelf '{shelf.name}'",
    )

    return shelf


# ----------------------------------------
# Remove Book from Shelf
# ----------------------------------------

def remove_book_from_shelf(
    db: Session,
    current_user: User,
    shelf_id: int,
    book_id: int,
):
    PermissionService.require_editor(
        db=db,
        shelf_id=shelf_id,
        user_id=current_user.id,
    )

    shelf = ShelfRepository.get_by_id_without_owner(
        db=db,
        shelf_id=shelf_id,
    )

    book = BookRepository.get_by_id_any(
        db=db,
        book_id=book_id,
    )

    if not book:
        raise HTTPException(
            status_code=404,
            detail="Book not found",
        )

    ShelfRepository.remove_book(
        db=db,
        shelf=shelf,
        book=book,
    )

    log_activity(
        db=db,
        current_user=current_user,
        action="BOOK_REMOVED_FROM_SHELF",
        message=f"{current_user.name} removed '{book.title}' from shelf '{shelf.name}'",
    )

    return shelf


# ----------------------------------------
# List Books in Shelf
# ----------------------------------------

def list_books_in_shelf(
    db: Session,
    current_user: User,
    shelf_id: int,
):
    PermissionService.require_viewer(
        db=db,
        shelf_id=shelf_id,
        user_id=current_user.id,
    )

    shelf = ShelfRepository.get_by_id_without_owner(
        db=db,
        shelf_id=shelf_id,
    )

    return ShelfRepository.list_books(shelf)