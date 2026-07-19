from sqlalchemy.orm import Session

# Activity database model
from app.models.activity import Activity


# Create a new activity record
def create_activity(
    db: Session,
    user_id: int,
    action: str,
    message: str,
) -> Activity:
    # Create a new Activity object
    activity = Activity(
        user_id=user_id,
        action=action,
        message=message,
    )

    # Save the activity to the database
    db.add(activity)
    db.commit()
    db.refresh(activity)

    # Return the saved activity
    return activity


# Get all activities ordered by the latest first
def get_all_activities(
    db: Session,
):
    return (
        db.query(Activity)
        .order_by(Activity.created_at.desc())
        .all()
    )


# Get activities for a specific user
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