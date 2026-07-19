from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship

# Base class for all database models
from app.db.database import Base


# Lending model to track borrowed books
class Lending(Base):
    # Database table name
    __tablename__ = "lendings"

    # Unique identifier for each lending record
    id = Column(Integer, primary_key=True, index=True)

    # Reference to the borrowed book
    book_id = Column(
        Integer,
        ForeignKey("books.id", ondelete="CASCADE"),
        nullable=False,
    )

    # User who owns the book
    owner_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )

    # User who borrowed the book
    borrower_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )

    # Date and time when the book was lent
    lent_at = Column(
        DateTime,
        default=datetime.utcnow,
    )

    # Date and time when the book was returned
    returned_at = Column(
        DateTime,
        nullable=True,
    )

    # Relationships
    # Linked book information
    book = relationship("Book")

    # Owner of the book
    owner = relationship(
        "User",
        foreign_keys=[owner_id],
    )

    # Borrower of the book
    borrower = relationship(
        "User",
        foreign_keys=[borrower_id],
    )