from fastapi import FastAPI

from app.api.auth import router as auth_router
from app.api.user import router as users_router
from app.api.book import router as book_router
from app.api.shelf import router as shelf_router

from app.db.database import Base, engine

# Import all models so SQLAlchemy creates the tables
from app.models.user import User
from app.models.book import Book
from app.models.shelf import Shelf

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI application
app = FastAPI(
    title="BookNest API",
)

# Register Routers
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(book_router)
app.include_router(shelf_router)


@app.get("/")
def home():
    return {
        "message": "Welcome to BookNest API"
    }