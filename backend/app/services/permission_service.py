from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.share_role import ShelfRole

from app.repositories.shelf_repository import ShelfRepository
from app.repositories.shelf_share_repository import ShelfShareRepository


class PermissionService:

    @staticmethod
    def get_role(
        db: Session,
        shelf_id: int,
        user_id: int,
    ):
        shelf = ShelfRepository.get_by_id_without_owner(
            db=db,
            shelf_id=shelf_id,
        )

        if shelf is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Shelf not found.",
            )

        # Shelf owner has full permissions
        if shelf.owner_id == user_id:
            return ShelfRole.OWNER

        # Check if the user has a shared role
        share = ShelfShareRepository.get_user_role(
            db=db,
            shelf_id=shelf_id,
            user_id=user_id,
        )

        if share is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to access this shelf.",
            )

        return share.role

    @staticmethod
    def require_viewer(
        db: Session,
        shelf_id: int,
        user_id: int,
    ):
        return PermissionService.get_role(
            db=db,
            shelf_id=shelf_id,
            user_id=user_id,
        )

    @staticmethod
    def require_editor(
        db: Session,
        shelf_id: int,
        user_id: int,
    ):
        role = PermissionService.get_role(
            db=db,
            shelf_id=shelf_id,
            user_id=user_id,
        )

        if role not in (
            ShelfRole.OWNER,
            ShelfRole.EDITOR,
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to modify this shelf. Only the shelf owner or an editor can add or remove books.",
            )

        return role

    @staticmethod
    def require_owner(
        db: Session,
        shelf_id: int,
        user_id: int,
    ):
        role = PermissionService.get_role(
            db=db,
            shelf_id=shelf_id,
            user_id=user_id,
        )

        if role != ShelfRole.OWNER:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only the shelf owner can perform this action.",
            )

        return role