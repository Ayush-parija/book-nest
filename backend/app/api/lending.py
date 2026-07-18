from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User

from app.schemas.lending import (
    LendBookRequest,
    LendingResponse,
    ReturnBookResponse,
)

from app.services.lending_service import (
    lend_book,
    return_book,
    get_borrowed_books,
    get_lent_books,
)

router = APIRouter(
    prefix="/lending",
    tags=["Lending"],
)


@router.get("/borrowed")
def borrowed_books(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_borrowed_books(
        db=db,
        current_user=current_user,
    )


@router.get("/lent")
def lent_books(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_lent_books(
        db=db,
        current_user=current_user,
    )


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