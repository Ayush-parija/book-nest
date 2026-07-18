from sqlalchemy.orm import Session

from app.models.activity import Activity


def create_activity(
    db: Session,
    user_id: int,
    action: str,
    message: str,
) -> Activity:
    activity = Activity(
        user_id=user_id,
        action=action,
        message=message,
    )

    db.add(activity)
    db.commit()
    db.refresh(activity)

    return activity


def get_all_activities(
    db: Session,
):
    return (
        db.query(Activity)
        .order_by(Activity.created_at.desc())
        .all()
    )


def get_user_activities(
    db: Session,
    user_id: int,
):
    return (
        db.query(Activity)
        .filter(Activity.user_id == user_id)
        .order_by(Activity.created_at.desc())
        .all()
    )