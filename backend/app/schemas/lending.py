from datetime import datetime

from pydantic import BaseModel, EmailStr, ConfigDict


# -----------------------------
# Lend Book Request
# -----------------------------
class LendBookRequest(BaseModel):
    email: EmailStr


# -----------------------------
# Return Book Response
# -----------------------------
class ReturnBookResponse(BaseModel):
    message: str


# -----------------------------
# Lending Response
# -----------------------------
class LendingResponse(BaseModel):
    id: int
    book_id: int
    book_title: str
    borrower_email: str
    owner_email: str
    lent_at: datetime
    returned_at: datetime | None

    model_config = ConfigDict(
        from_attributes=True,
    )


# -----------------------------
# Borrowed Book Response
# -----------------------------
class BorrowedBookResponse(BaseModel):
    lending_id: int
    book_id: int
    title: str
    author: str
    owner_name: str
    lent_at: datetime