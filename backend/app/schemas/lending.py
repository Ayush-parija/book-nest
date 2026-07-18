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


from pydantic import BaseModel, EmailStr, ConfigDict, model_validator

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

    @model_validator(mode="before")
    @classmethod
    def extract_relations(cls, data):
        if not isinstance(data, dict) and hasattr(data, "book"):
            return {
                "id": data.id,
                "book_id": data.book_id,
                "book_title": data.book.title if data.book else "",
                "borrower_email": data.borrower.email if data.borrower else "",
                "owner_email": data.owner.email if data.owner else "",
                "lent_at": data.lent_at,
                "returned_at": data.returned_at,
            }
        return data


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