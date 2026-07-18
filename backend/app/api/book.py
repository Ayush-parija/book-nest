from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.dependencies.auth import get_current_user

from app.models.enums import BookStatus
from app.models.user import User

from app.schemas.book import (
    BookCreate,
    BookUpdate,
    BookResponse,
    ReadingProgressUpdate,
)

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

router = APIRouter(
    prefix="/books",
    tags=["Books"],
)


# =====================================================
# BOOK CRUD
# =====================================================

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