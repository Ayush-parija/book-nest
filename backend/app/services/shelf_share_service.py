from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User

from app.models.share_role import ShelfRole

from app.repositories.user_repository import UserRepository
from app.repositories.shelf_share_repository import ShelfShareRepository

from app.services.permission_service import PermissionService
from app.services.activity_service import log_activity

from app.schemas.shelf_share import ShelfShareCreate


def share_shelf(
    db: Session,
    current_user: User,
    shelf_id: int,
    data: ShelfShareCreate,
):
    # Only owner can share
    PermissionService.require_owner(
        db=db,
        shelf_id=shelf_id,
        user_id=current_user.id,
    )

    shelf = ShelfShareRepository.get_shelf(
        db=db,
        shelf_id=shelf_id,
    )

    if shelf is None:
        raise HTTPException(
            status_code=404,
            detail="Shelf not found",
        )

    # Find user by email
    user = UserRepository.get_by_email(
        email=data.email,
        db=db,
    )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    # Prevent sharing with yourself
    if user.id == current_user.id:
        raise HTTPException(
            status_code=400,
            detail="You cannot share a shelf with yourself.",
        )

    # Already shared?
    existing = ShelfShareRepository.get_collaborator(
        db=db,
        shelf_id=shelf_id,
        user_id=user.id,
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Shelf already shared with this user.",
        )

    ShelfShareRepository.create_share(
        db=db,
        shelf_id=shelf_id,
        user_id=user.id,
        role=data.role,
    )

    log_activity(
        db=db,
        current_user=current_user,
        action="SHELF_SHARED",
        message=f"{current_user.name} shared '{shelf.name}' with {user.name} as {data.role.value}.",
    )

    return {
        "message": "Shelf shared successfully."
    }

from app.schemas.shelf_share import ShelfShareUpdate

def update_share_role(
    db: Session,
    current_user: User,
    shelf_id: int,
    collaborator_id: int,
    data: ShelfShareUpdate,
):
    PermissionService.require_owner(
        db=db,
        shelf_id=shelf_id,
        user_id=current_user.id,
    )

    collaborator = ShelfShareRepository.get_collaborator(
        db=db,
        shelf_id=shelf_id,
        user_id=collaborator_id,
    )

    if collaborator is None:
        raise HTTPException(
            status_code=404,
            detail="Collaborator not found.",
        )

    updated = ShelfShareRepository.update_role(
        db=db,
        share=collaborator,
        role=data.role,
    )

    log_activity(
        db=db,
        current_user=current_user,
        action="COLLABORATOR_ROLE_UPDATED",
        message=f"Updated collaborator role to {data.role.value}.",
    )

    return {
        "message": "Collaborator role updated successfully.",
        "role": updated.role,
    }

def remove_collaborator(
    db: Session,
    current_user: User,
    shelf_id: int,
    collaborator_id: int,
):
    PermissionService.require_owner(
        db=db,
        shelf_id=shelf_id,
        user_id=current_user.id,
    )

    collaborator = ShelfShareRepository.get_collaborator(
        db=db,
        shelf_id=shelf_id,
        user_id=collaborator_id,
    )

    if collaborator is None:
        raise HTTPException(
            status_code=404,
            detail="Collaborator not found.",
        )

    ShelfShareRepository.remove_share(
        db=db,
        collaborator=collaborator,
    )

    log_activity(
        db=db,
        current_user=current_user,
        action="COLLABORATOR_REMOVED",
        message="Removed collaborator from shelf.",
    )

    return {
        "message": "Collaborator removed successfully."
    }

from app.schemas.shelf_share import SharedShelfResponse

def shared_with_me(
    db: Session,
    current_user: User,
):
    results = ShelfShareRepository.get_shared_shelves(
        db=db,
        user_id=current_user.id,
    )

    response = []

    for shelf, share, owner in results:
        response.append(
            SharedShelfResponse(
                id=shelf.id,
                name=shelf.name,
                owner_name=owner.name,
                role=share.role,
            )
        )

    return response