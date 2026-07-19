# Import database models
from app.models.user import User
from app.models.book import Book
from app.models.shelf import Shelf

# Export models when using "from app.models import *"
__all__ = [
    "User",
    "Book",
    "Shelf",
]