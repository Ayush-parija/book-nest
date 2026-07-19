from pydantic import BaseModel, ConfigDict
from typing import Any

# Response schemas used in the dashboard
from app.schemas.book import BookResponse
from app.schemas.shelf import ShelfResponse
from app.schemas.stats import StatsResponse
from app.schemas.activity import ActivityResponse
from app.schemas.shelf_share import SharedShelfResponse
from app.schemas.lending import LendingResponse


# Basic user information displayed on the dashboard
class UserDashboard(BaseModel):
    # User ID
    id: int

    # User name
    name: str

    # User email address
    email: str

    # Enable conversion from SQLAlchemy models
    model_config = ConfigDict(from_attributes=True)


# Complete dashboard response
class DashboardResponse(BaseModel):
    # Logged-in user details
    user: UserDashboard

    # Reading statistics
    statistics: StatsResponse

    # Books currently being read
    currently_reading: list[BookResponse]

    # User's favorite books
    favorite_books: list[BookResponse]

    # Recently added books
    recent_books: list[BookResponse]

    # User's shelves
    shelves: list[ShelfResponse]

    # Books lent to other users
    lent_books: list[LendingResponse]

    # Shelves shared with the user
    shared_shelves: list[SharedShelfResponse]

    # Recent activity history
    activity_feed: list[ActivityResponse]