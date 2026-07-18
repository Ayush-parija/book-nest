from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import BookStatus


class BookCreate(BaseModel):
    title: str
    author: str
    status: BookStatus = BookStatus.WANT_TO_READ
    total_pages: int | None = None
    rating: int | None = Field(None, ge=1, le=5)
    notes: str | None = None


class BookUpdate(BaseModel):
    title: str | None = None
    author: str | None = None
    status: BookStatus | None = None
    total_pages: int | None = None
    current_page: int | None = None
    rating: int | None = Field(None, ge=1, le=5)
    notes: str | None = None


class ReadingProgressUpdate(BaseModel):
    current_page: int = Field(..., ge=0)


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
    finished_at: datetime | None
    is_favorite: bool

    model_config = ConfigDict(from_attributes=True)