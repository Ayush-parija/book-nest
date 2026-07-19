from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

# Dependency to get the currently authenticated user
from app.dependencies.auth import get_current_user

# Database session dependency
from app.dependencies.database import get_db

# User model
from app.models.user import User

# Dashboard response schema
from app.schemas.dashboard import DashboardResponse

# Service function that prepares dashboard data
from app.services.dashboard_service import get_dashboard

# Router for dashboard-related endpoints
router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


# Returns dashboard statistics for the logged-in user
@router.get(
    "",
    response_model=DashboardResponse,
)
def dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Fetch dashboard data from the service layer
    return get_dashboard(
        db=db,
        current_user=current_user,
    )