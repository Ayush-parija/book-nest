from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

# Import database session dependency
from app.db.dependencies import get_db

# Import dependency to get the currently logged-in user
from app.dependencies.auth import get_current_user

# User model
from app.models.user import User

# Response schema for activity API
from app.schemas.activity import ActivityResponse

# Import activity service functions
from app.services.activity_service import (
    get_activity_feed,
    get_my_activities,
)

# Activity router configuration
router = APIRouter(
    prefix="/activity",
    tags=["Activity"],
)


# Returns the complete activity feed
@router.get(
    "",
    response_model=list[ActivityResponse],
)
def activity_feed(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Call service layer to fetch all activities
    return get_activity_feed(db)


# Returns activities of the logged-in user only
@router.get(
    "/me",
    response_model=list[ActivityResponse],
)
def my_activity(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Call service layer to fetch current user's activities
    return get_my_activities(
        db=db,
        current_user=current_user,
    )