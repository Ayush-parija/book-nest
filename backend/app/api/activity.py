from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User

from app.schemas.activity import ActivityResponse
from app.services.activity_service import (
    get_activity_feed,
    get_my_activities,
)

router = APIRouter(
    prefix="/activity",
    tags=["Activity"],
)


@router.get(
    "",
    response_model=list[ActivityResponse],
)
def activity_feed(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_activity_feed(db)


@router.get(
    "/me",
    response_model=list[ActivityResponse],
)
def my_activity(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_my_activities(
        db=db,
        current_user=current_user,
    )