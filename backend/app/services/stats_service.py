from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.stats_repository import StatsRepository


def get_statistics(
    db: Session,
    current_user: User,
):
    return StatsRepository.get_stats(
        db=db,
        owner_id=current_user.id,
    )