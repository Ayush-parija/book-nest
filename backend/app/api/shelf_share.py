from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies.auth import get_current_user
from app.dependencies.database import get_db

from app.models.user import User

from app.schemas.shelf_share import (
    ShelfShareCreate,
    ShelfShareUpdate,
    SharedShelfResponse,
)

from app.services.shelf_share_service import (
    share_shelf,
    update_share_role,
    remove_collaborator,
    shared_with_me,
)

# shelf_share.py
router = APIRouter(
    prefix="/shared-shelves",
    tags=["Shared Shelves"],
)

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


