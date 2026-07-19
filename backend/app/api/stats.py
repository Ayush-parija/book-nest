from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

# Database session dependency
from app.db.dependencies import get_db

# Dependency to get the currently authenticated user
from app.dependencies.auth import get_current_user

# User model
from app.models.user import User

# Response schema for statistics
from app.schemas.stats import StatsResponse

# Service function that calculates user statistics
from app.services.stats_service import get_statistics

# Router for statistics-related endpoints
router = APIRouter(
    prefix="/stats",
    tags=["Statistics"],
)


# Get statistics for the logged-in user
@router.get(
    "",
    response_model=StatsResponse,
)
def get_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Fetch and return statistics from the service layer
    return get_statistics(
        db=db,
        current_user=current_user,
    )