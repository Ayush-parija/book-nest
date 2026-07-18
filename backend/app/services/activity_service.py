from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.activity_repository import (
    create_activity,
    get_all_activities,
    get_user_activities,
)
from app.websocket.connection_manager import manager


def log_activity(
    db: Session,
    current_user: User,
    action: str,
    message: str,
):
    """
    Create a new activity log and broadcast it.
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


def get_activity_feed(db: Session):
    return get_all_activities(db)


def get_my_activities(
    db: Session,
    current_user: User,
):
    return get_user_activities(
        db=db,
        user_id=current_user.id,
    )