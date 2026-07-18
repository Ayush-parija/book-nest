# =========================================================
# File: dashboard_service.py
# Purpose:
# Aggregates data from various repositories to build the dashboard view.
#
# Responsibilities:
# - Fetch user statistics
# - Fetch currently reading books
# - Fetch favorite and recent books
# - Fetch user shelves
#
# Depends on:
# - DashboardRepository
# - User model
#
# Used by:
# - Dashboard router (dashboard.py)
# =========================================================

# Navigation
# [1] Third-party Libraries
# [2] Local Models
# [3] Repositories
# [4] Dashboard Logic

# =====================================================
# [1] Third-party Libraries
# =====================================================
from sqlalchemy.orm import Session

# =====================================================
# [2] Local Models
# =====================================================
from app.models.user import User

# =====================================================
# [3] Repositories
# =====================================================
from app.repositories.dashboard_repository import DashboardRepository


# =====================================================
# [4] Dashboard Logic
# =====================================================

def get_dashboard(
    db: Session,
    current_user: User,
):
    """
    ---------------------------------------------------------
    Function:
    get_dashboard()

    Purpose:
    Retrieves all necessary data to render the user's main dashboard.
    This includes user details, reading statistics, current books, 
    favorites, recent additions, and shelves.

    Parameters:
    db: Database session
    current_user: The authenticated User instance

    Returns:
    dict: A dictionary containing all aggregated dashboard data

    Raises:
    None

    Side Effects:
    - Executes multiple read queries against the database via DashboardRepository
    ---------------------------------------------------------
    """
    return {
        "user": DashboardRepository.get_user(
            db=db,
            user_id=current_user.id,
        ),
        "statistics": DashboardRepository.get_statistics(
            db=db,
            owner_id=current_user.id,
        ),
        "currently_reading": DashboardRepository.get_currently_reading(
            db=db,
            owner_id=current_user.id,
        ),
        "favorite_books": DashboardRepository.get_favorite_books(
            db=db,
            owner_id=current_user.id,
        ),
        "recent_books": DashboardRepository.get_recent_books(
            db=db,
            owner_id=current_user.id,
        ),
        "shelves": DashboardRepository.get_shelves(
            db=db,
            owner_id=current_user.id,
        ),
    }