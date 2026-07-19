from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

# Dependency to get the currently logged-in user
from app.dependencies.auth import get_current_user

# Database session dependency
from app.dependencies.database import get_db

# User model
from app.models.user import User

# Request and response schemas for shelf sharing
from app.schemas.shelf_share import (
    ShelfShareCreate,
    ShelfShareUpdate,
    SharedShelfResponse,
    ShelfCollaboratorResponse,
)

# Service functions for shelf sharing operations
from app.services.shelf_share_service import (
    share_shelf,
    update_share_role,
    remove_collaborator,
    shared_with_me,
    get_collaborators,
)

# Router for shared shelf related APIs
# shelf_share.py
router = APIRouter(
    prefix="/shared-shelves",
    tags=["Shared Shelves"],
)

# Get all shelves that have been shared with the current user
@router.get(
    "/shared",
    response_model=list[SharedShelfResponse],
)
def shared(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return shared_with_me(
        db=db,
        current_user=current_user,
    )

# Get the list of collaborators for a specific shelf
@router.get(
    "/{shelf_id}/collaborators",
    response_model=list[ShelfCollaboratorResponse],
)
def get_shelf_collaborators(
    shelf_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_collaborators(
        db=db,
        current_user=current_user,
        shelf_id=shelf_id,
    )

# Share a shelf with another user
@router.post("/{shelf_id}/share")
def share(
    shelf_id: int,
    data: ShelfShareCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return share_shelf(
        db=db,
        current_user=current_user,
        shelf_id=shelf_id,
        data=data,
    )


# Update the role of an existing collaborator
@router.patch("/{shelf_id}/share/{collaborator_id}")
def update_role(
    shelf_id: int,
    collaborator_id: int,
    data: ShelfShareUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return update_share_role(
        db=db,
        current_user=current_user,
        shelf_id=shelf_id,
        collaborator_id=collaborator_id,
        data=data,
    )


# Remove a collaborator from the shared shelf
@router.delete("/{shelf_id}/share/{collaborator_id}")
def remove(
    shelf_id: int,
    collaborator_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return remove_collaborator(
        db=db,
        current_user=current_user,
        shelf_id=shelf_id,
        collaborator_id=collaborator_id,
    )