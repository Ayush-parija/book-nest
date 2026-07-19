from sqlalchemy.orm import Session

# Database models
from app.models.shelf import Shelf
from app.models.shelf_share import ShelfShare
from app.models.share_role import ShelfRole
from app.models.user import User


# Repository class for handling shelf sharing operations
class ShelfShareRepository:

    # Get a shelf by its ID
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

    # Find a user using their email address
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

    # Get a specific collaborator for a shelf
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

    # Get all collaborators assigned to a shelf
    @staticmethod
    def get_all_collaborators(
        db: Session,
        shelf_id: int,
    ):
        return (
            db.query(ShelfShare)
            .filter(ShelfShare.shelf_id == shelf_id)
            .all()
        )

    # Get collaborator details along with user information
    @staticmethod
    def get_collaborators_with_users(
        db: Session,
        shelf_id: int,
    ):
        return (
            db.query(ShelfShare, User)
            .join(User, User.id == ShelfShare.user_id)
            .filter(ShelfShare.shelf_id == shelf_id)
            .all()
        )

    # Share a shelf with a user
    @staticmethod
    def create_share(
        db: Session,
        shelf_id: int,
        user_id: int,
        role: ShelfRole,
    ):
        # Create a new sharing record
        share = ShelfShare(
            shelf_id=shelf_id,
            user_id=user_id,
            role=role,
        )

        # Save the sharing information
        db.add(share)
        db.commit()
        db.refresh(share)

        return share

    # Update the collaborator's role
    @staticmethod
    def update_role(
        db: Session,
        share: ShelfShare,
        role: ShelfRole,
    ):
        # Change the assigned role
        share.role = role

        db.commit()
        db.refresh(share)

        return share

    # Remove a collaborator from a shelf
    @staticmethod
    def remove_share(
        db: Session,
        share: ShelfShare,
    ):
        db.delete(share)
        db.commit()

    # Get all shelves shared with a specific user
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

    # Get the role of a user for a particular shelf
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