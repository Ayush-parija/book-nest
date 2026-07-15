from datetime import datetime
from pydantic import BaseModel, ConfigDict
from app.models.enums import BookStatus


class BookCreate(BaseModel):
    title: str
    author: str
    status: BookStatus = BookStatus.WANT_TO_READ
    total_pages: int | None = None
    rating: int | None = None
    notes: str | None = None


class BookUpdate(BaseModel):
    title: str | None = None
    author: str | None = None
    status: BookStatus | None = None
    total_pages: int | None = None
    current_page: int | None = None
    rating: int | None = None
    notes: str | None = None


class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    status: BookStatus
    total_pages: int | None
    current_page: int | None
    rating: int | None
    notes: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)