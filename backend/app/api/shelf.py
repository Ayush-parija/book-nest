from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.dependencies.auth import get_current_user

from app.schemas.shelf_share import ShelfShareCreate
from app.services.shelf_share_service import share_shelf

from app.models.user import User

from app.schemas.book import BookResponse
from app.schemas.shelf import (
    ShelfCreate,
    ShelfUpdate,
    ShelfResponse,
)

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

router = APIRouter(
    prefix="/shelves",
    tags=["Shelves"],
)


# -----------------------------
# Shelf CRUD
# -----------------------------

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