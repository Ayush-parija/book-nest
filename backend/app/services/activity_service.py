# =========================================================
# File: activity_service.py
# Purpose:
# Handles the creation and retrieval of user activity logs.
#
# Responsibilities:
# - Log user actions (e.g., lending, returning, adding books)
# - Broadcast real-time notifications via WebSockets
# - Fetch global activity feeds
# - Fetch user-specific activity history
#
# Depends on:
# - ActivityRepository
# - ConnectionManager (WebSockets)
# - User model
#
# Used by:
# - Activity router (activity.py)
# - Other services (e.g., lending_service.py, book_service.py)
# =========================================================

# Navigation
# [1] Third-party Libraries
# [2] Local Models
# [3] Repositories
# [4] WebSockets
# [5] Activity Logging
# [6] Activity Retrieval

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
from app.repositories.activity_repository import (
    create_activity,
    get_all_activities,
    get_user_activities,
)

# =====================================================
# [4] WebSockets
# =====================================================
from app.websocket.connection_manager import manager


# =====================================================
# [5] Activity Logging
# =====================================================

def log_activity(
    db: Session,
    current_user: User,
    action: str,
    message: str,
):
    """
    ---------------------------------------------------------
    Function:
    log_activity()

    Purpose:
    Creates a new activity log in the database and broadcasts 
    a real-time notification to all connected users.

    Parameters:
    db: Database session
    current_user: User instance of the person performing the action
    action: Short string representing the action type (e.g., "BOOK_LENT")
    message: Human-readable description of the activity

    Returns:
    Activity: The newly created Activity database model

    Raises:
    None

    Side Effects:
    - Inserts a record into the activities table
    - Broadcasts a WebSocket message via ConnectionManager
    ---------------------------------------------------------
    """
    activity = create_activity(
        db=db,
        user_id=current_user.id,
        action=action,
        message=message,
    )

    print("Active connections:", len(manager.active_connections))

    if manager.active_connections:
        manager.broadcast_sync(
            f"{current_user.name}: {action} - {message}"
        )

    return activity


# =====================================================
# [6] Activity Retrieval
# =====================================================

def get_activity_feed(db: Session):
    """
    ---------------------------------------------------------
    Function:
    get_activity_feed()

    Purpose:
    Retrieves the global feed of all public activities.

    Parameters:
    db: Database session

    Returns:
    list[Activity]: A list of recent activities

    Raises:
    None

    Side Effects:
    None
    ---------------------------------------------------------
    """
    return get_all_activities(db)


def get_my_activities(
    db: Session,
    current_user: User,
):
    """
    ---------------------------------------------------------
    Function:
    get_my_activities()

    Purpose:
    Retrieves the activity history specific to the authenticated user.

    Parameters:
    db: Database session
    current_user: The authenticated User instance

    Returns:
    list[Activity]: A list of the user's activities

    Raises:
    None

    Side Effects:
    None
    ---------------------------------------------------------
    """
    return get_user_activities(
        db=db,
        user_id=current_user.id,
    )