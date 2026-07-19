from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

# Database session dependency
from app.dependencies.database import get_db

# Dependency to get the currently authenticated user
from app.dependencies.auth import get_current_user

# Schema used when sharing a shelf
from app.schemas.shelf_share import ShelfShareCreate

# Service function for sharing shelves
from app.services.shelf_share_service import share_shelf

# User model
from app.models.user import User

# Response schema for books
from app.schemas.book import BookResponse

# Request and response schemas for shelves
from app.schemas.shelf import (
    ShelfCreate,
    ShelfUpdate,
    ShelfResponse,
)

# Shelf-related business logic
from app.services.shelf_service import (
    create_shelf,
    get_shelves,
    get_shelf,
    update_shelf,
    delete_shelf,
    add_book_to_shelf,
    remove_book_from_shelf,
    list_books_in_shelf,
)

# Router for all shelf-related endpoints
router = APIRouter(
    prefix="/shelves",
    tags=["Shelves"],
)


# -----------------------------
# Shelf CRUD
# -----------------------------

# Create a new shelf
@router.post(
    "",
    response_model=ShelfResponse,
    status_code=201,
)
def create_new_shelf(
    data: ShelfCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_shelf(
        db=db,
        current_user=current_user,
        data=data,
    )


# Get all shelves that belong to the current user
@router.get(
    "",
    response_model=list[ShelfResponse],
)
def list_shelves(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_shelves(
        db=db,
        current_user=current_user,
    )


# Get details of a specific shelf
@router.get(
    "/{shelf_id}",
    response_model=ShelfResponse,
)
def get_single_shelf(
    shelf_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_shelf(
        db=db,
        current_user=current_user,
        shelf_id=shelf_id,
    )


# Update an existing shelf
@router.patch(
    "/{shelf_id}",
    response_model=ShelfResponse,
)
def edit_shelf(
    shelf_id: int,
    data: ShelfUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return update_shelf(
        db=db,
        current_user=current_user,
        shelf_id=shelf_id,
        data=data,
    )


# Delete a shelf
@router.delete(
    "/{shelf_id}",
)
def remove_shelf(
    shelf_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return delete_shelf(
        db=db,
        current_user=current_user,
        shelf_id=shelf_id,
    )


# Share a shelf with another user
@router.post("/{shelf_id}/share")
def share_shelf_api(
    shelf_id: int,
    data: ShelfShareCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return share_shelf(
        db=db,
        current_user=current_user,
        shelf_id=shelf_id,
        data=data,
    )


# -----------------------------
# Book ↔ Shelf APIs
# -----------------------------

# Add a book to a shelf
@router.post(
    "/{shelf_id}/books/{book_id}",
)
def add_book(
    shelf_id: int,
    book_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return add_book_to_shelf(
        db=db,
        current_user=current_user,
        shelf_id=shelf_id,
        book_id=book_id,
    )


# Remove a book from a shelf
@router.delete(
    "/{shelf_id}/books/{book_id}",
)
def remove_book(
    shelf_id: int,
    book_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return remove_book_from_shelf(
        db=db,
        current_user=current_user,
        shelf_id=shelf_id,
        book_id=book_id,
    )


# Get all books available in a specific shelf
@router.get(
    "/{shelf_id}/books",
    response_model=list[BookResponse],
)
def get_books_in_shelf(
    shelf_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return list_books_in_shelf(
        db=db,
        current_user=current_user,
        shelf_id=shelf_id,
    )