from fastapi import APIRouter, Depends

from app.core.dependencies import get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get("/me")
def me(
    current_user: User = Depends(get_current_user),
):
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "total_books": len(current_user.books),
        "total_shelves": len(current_user.shelves),
        "books": [
            {
                "id": book.id,
                "title": book.title,
                "author": book.author,
                "status": book.status,
            }
            for book in current_user.books
        ],
        "shelves": [
            {
                "id": shelf.id,
                "name": shelf.name,
            }
            for shelf in current_user.shelves
        ],
    }