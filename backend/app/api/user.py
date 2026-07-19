from fastapi import APIRouter, Depends

# Dependency to get the currently authenticated user
from app.core.dependencies import get_current_user

# User model
from app.models.user import User

# Router for user-related endpoints
router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


# Get the profile details of the logged-in user
@router.get("/me")
def me(
    current_user: User = Depends(get_current_user),
):
    # Return user information along with books and shelves
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "total_books": len(current_user.books),
        "total_shelves": len(current_user.shelves),

        # List of books owned by the user
        "books": [
            {
                "id": book.id,
                "title": book.title,
                "author": book.author,
                "status": book.status,
            }
            for book in current_user.books
        ],

        # List of shelves created by the user
        "shelves": [
            {
                "id": shelf.id,
                "name": shelf.name,
            }
            for shelf in current_user.shelves
        ],
    }