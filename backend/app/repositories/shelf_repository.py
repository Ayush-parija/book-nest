from sqlalchemy.orm import Session
from sqlalchemy import or_

# Database models
from app.models.book import Book
from app.models.shelf import Shelf

# Request schemas for creating and updating shelves
from app.schemas.shelf import ShelfCreate, ShelfUpdate

# Shelf sharing model
from app.models.shelf_share import ShelfShare


# Repository class for handling shelf-related database operations
class ShelfRepository:

    # Create a new shelf
    @staticmethod
    def create(
        db: Session,
        owner_id: int,
        data: ShelfCreate,
    ):
        # Create a new Shelf object
        shelf = Shelf(
            name=data.name,
            owner_id=owner_id,
        )

        # Save the shelf to the database
        db.add(shelf)
        db.commit()
        db.refresh(shelf)

        return shelf

    # Get all shelves owned by a user
    @staticmethod
    def get_all(
        db: Session,
        user_id: int,
    ):
        return (
            db.query(Shelf)
            .filter(Shelf.owner_id == user_id)
            .all()
        )

    # Get a specific shelf belonging to a user
    @staticmethod
    def get_by_id(
        db: Session,
        shelf_id: int,
        owner_id: int,
    ):
        return (
            db.query(Shelf)
            .filter(
                Shelf.id == shelf_id,
                Shelf.owner_id == owner_id,
            )
            .first()
        )

    # Update shelf details
    @staticmethod
    def update(
        db: Session,
        shelf: Shelf,
        data: ShelfUpdate,
    ):
        # Get only the provided fields
        update_data = data.model_dump(exclude_unset=True)

        # Update shelf attributes dynamically
        for key, value in update_data.items():
            setattr(shelf, key, value)

        db.commit()
        db.refresh(shelf)

        return shelf

    # Delete a shelf
    @staticmethod
    def delete(
        db: Session,
        shelf: Shelf,
    ):
        db.delete(shelf)
        db.commit()

    # -------------------------
    # Book ↔ Shelf
    # -------------------------

    # Add a book to a shelf
    @staticmethod
    def add_book(
        db: Session,
        shelf: Shelf,
        book: Book,
    ):
        # Avoid adding duplicate books
        if book not in shelf.books:
            shelf.books.append(book)
            db.commit()
            db.refresh(shelf)

        return shelf

    # Remove a book from a shelf
    @staticmethod
    def remove_book(
        db: Session,
        shelf: Shelf,
        book: Book,
    ):
        # Remove the book only if it exists
        if book in shelf.books:
            shelf.books.remove(book)
            db.commit()
            db.refresh(shelf)

        return shelf

    # Get all books in a shelf
    @staticmethod
    def list_books(
        shelf: Shelf,
    ):
        return shelf.books

    # Get a shelf by ID without checking ownership
    @staticmethod
    def get_by_id_without_owner(
    db: Session,
    shelf_id: int,
    ):
        return (
            db.query(Shelf)
            .filter(
                Shelf.id == shelf_id,
            )
            .first()
        )

    # Get all shelves owned by a specific user
    @staticmethod
    def get_owned_shelves(
        db: Session,
        owner_id: int,
    ):
        return (
            db.query(Shelf)
            .filter(
                Shelf.owner_id == owner_id,
            )
            .all()
        )

    # Get shelves shared with a user
    @staticmethod
    def get_shared_shelves(
        db: Session,
        user_id: int,
    ):
        return (
            db.query(Shelf)
            .join(
                ShelfShare,
                Shelf.id == ShelfShare.shelf_id,
            )
            .filter(
                ShelfShare.user_id == user_id,
            )
            .all()
        )