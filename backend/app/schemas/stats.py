from pydantic import BaseModel


# Response schema for user reading statistics
class StatsResponse(BaseModel):
    # Total number of books
    total_books: int

    # Number of books marked as "Want to Read"
    want_to_read: int

    # Number of books currently being read
    reading: int

    # Number of completed books
    finished: int

    # Total pages read across all books
    total_pages_read: int

    # Average rating of all rated books
    average_rating: float

    # Number of books finished in the current year
    finished_this_year: int

    # Name of the shelf with the most books
    largest_shelf: str | None = None