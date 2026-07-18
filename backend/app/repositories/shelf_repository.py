from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models.book import Book
from app.models.shelf import Shelf
from app.schemas.shelf import ShelfCreate, ShelfUpdate

from app.models.shelf_share import ShelfShare


class ShelfRepository:

    @staticmethod
    def create(
        db: Session,
        owner_id: int,
        data: ShelfCreate,
    ):
        shelf = Shelf(
            name=data.name,
            owner_id=owner_id,
        )

        db.add(shelf)
        db.commit()
        db.refresh(shelf)

        return shelf

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

    @staticmethod
    def update(
        db: Session,
        shelf: Shelf,
        data: ShelfUpdate,
    ):
        update_data = data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(shelf, key, value)

        db.commit()
        db.refresh(shelf)

        return shelf

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

    @staticmethod
    def add_book(
        db: Session,
        shelf: Shelf,
        book: Book,
    ):
        if book not in shelf.books:
            shelf.books.append(book)
            db.commit()
            db.refresh(shelf)

        return shelf

    @staticmethod
    def remove_book(
        db: Session,
        shelf: Shelf,
        book: Book,
    ):
        if book in shelf.books:
            shelf.books.remove(book)
            db.commit()
            db.refresh(shelf)

        return shelf

    @staticmethod
    def list_books(
        shelf: Shelf,
    ):
        return shelf.books
    
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