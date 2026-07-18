from sqlalchemy.orm import Session

from app.models.user import User

from app.repositories.dashboard_repository import DashboardRepository


def get_dashboard(
    db: Session,
    current_user: User,
):
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