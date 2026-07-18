from pydantic import BaseModel


class StatsResponse(BaseModel):
    total_books: int
    want_to_read: int
    reading: int
    finished: int
    total_pages_read: int
    average_rating: float
    finished_this_year: int
    largest_shelf: str | None = None