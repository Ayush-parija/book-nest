from datetime import datetime

from pydantic import BaseModel, EmailStr, ConfigDict


# -----------------------------
# Lend Book Request
# -----------------------------

# Request schema for lending a book
class LendBookRequest(BaseModel):
    # Email of the user who will borrow the book
    email: EmailStr


# -----------------------------
# Return Book Response
# -----------------------------

# Response returned after a successful book return
class ReturnBookResponse(BaseModel):
    # Confirmation message
    message: str


from pydantic import BaseModel, EmailStr, ConfigDict, model_validator

# -----------------------------
# Lending Response
# -----------------------------

# Response schema containing lending details
class LendingResponse(BaseModel):
    # Lending record ID
    id: int

    # ID of the borrowed book
    book_id: int

    # Title of the borrowed book
    book_title: str

    # Borrower's email address
    borrower_email: str

    # Owner's email address
    owner_email: str

    # Date and time when the book was lent
    lent_at: datetime

    # Date and time when the book was returned
    returned_at: datetime | None

    # Enable conversion from SQLAlchemy models
    model_config = ConfigDict(
        from_attributes=True,
    )

    # Extract related model data before validation
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

# Response schema for borrowed book details
class BorrowedBookResponse(BaseModel):
    # Lending record ID
    lending_id: int

    # Book ID
    book_id: int

    # Book title
    title: str

    # Book author
    author: str

    # Name of the book owner
    owner_name: str

    # Date and time when the book was lent
    lent_at: datetime