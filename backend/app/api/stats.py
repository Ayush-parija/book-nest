from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.dependencies.auth import get_current_user

from app.models.user import User

from app.schemas.stats import StatsResponse

from app.services.stats_service import get_statistics

router = APIRouter(
    prefix="/stats",
    tags=["Statistics"],
)


@router.get(
    "",
    response_model=StatsResponse,
)
def get_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_statistics(
        db=db,
        current_user=current_user,
    )