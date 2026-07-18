from sqlalchemy.orm import Session

from app.models.shelf import Shelf
from app.models.shelf_share import ShelfShare
from app.models.share_role import ShelfRole
from app.models.user import User


class ShelfShareRepository:

    @staticmethod
    def get_shelf(
        db: Session,
        shelf_id: int,
    ):
        return (
            db.query(Shelf)
            .filter(Shelf.id == shelf_id)
            .first()
        )

    @staticmethod
    def get_user_by_email(
        db: Session,
        email: str,
    ):
        return (
            db.query(User)
            .filter(User.email == email)
            .first()
        )

    @staticmethod
    def get_collaborator(
        db: Session,
        shelf_id: int,
        user_id: int,
    ):
        return (
            db.query(ShelfShare)
            .filter(
                ShelfShare.shelf_id == shelf_id,
                ShelfShare.user_id == user_id,
            )
            .first()
        )

    @staticmethod
    def create_share(
        db: Session,
        shelf_id: int,
        user_id: int,
        role: ShelfRole,
    ):
        share = ShelfShare(
            shelf_id=shelf_id,
            user_id=user_id,
            role=role,
        )

        db.add(share)
        db.commit()
        db.refresh(share)

        return share

    @staticmethod
    def update_role(
        db: Session,
        share: ShelfShare,
        role: ShelfRole,
    ):
        share.role = role

        db.commit()
        db.refresh(share)

        return share

    @staticmethod
    def remove_share(
        db: Session,
        share: ShelfShare,
    ):
        db.delete(share)
        db.commit()

    @staticmethod
    def get_shared_shelves(
        db: Session,
        user_id: int,
    ):
        return (
            db.query(
                Shelf,
                ShelfShare,
                User,
            )
            .join(
                ShelfShare,
                Shelf.id == ShelfShare.shelf_id,
            )
            .join(
                User,
                User.id == Shelf.owner_id,
            )
            .filter(
                ShelfShare.user_id == user_id,
            )
            .all()
        )

    @staticmethod
    def get_user_role(
        db: Session,
        shelf_id: int,
        user_id: int,
    ):
        return (
            db.query(ShelfShare)
            .filter(
                ShelfShare.shelf_id == shelf_id,
                ShelfShare.user_id == user_id,
            )
            .first()
        )