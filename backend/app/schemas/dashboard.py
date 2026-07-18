from pydantic import BaseModel, ConfigDict
from typing import Any

from app.schemas.book import BookResponse
from app.schemas.shelf import ShelfResponse
from app.schemas.stats import StatsResponse
from app.schemas.activity import ActivityResponse
from app.schemas.shelf_share import SharedShelfResponse


class UserDashboard(BaseModel):
    id: int
    name: str
    email: str

    model_config = ConfigDict(from_attributes=True)


class DashboardResponse(BaseModel):
    user: UserDashboard
    statistics: StatsResponse
    currently_reading: list[BookResponse]
    favorite_books: list[BookResponse]
    recent_books: list[BookResponse]
    shelves: list[ShelfResponse]
    lent_books: list[Any]
    shared_shelves: list[SharedShelfResponse]
    activity_feed: list[ActivityResponse]