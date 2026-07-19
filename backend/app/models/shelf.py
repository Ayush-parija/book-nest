from datetime import datetime
from app.models.shelf_share import ShelfShare

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    String,
    Table,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

# Base class for all database models
from app.db.database import Base


# Association table for the many-to-many relationship
# between books and shelves
book_shelves = Table(
    "book_shelves",
    Base.metadata,
    Column(
        "book_id",
        ForeignKey("books.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "shelf_id",
        ForeignKey("shelves.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


# Shelf model
class Shelf(Base):
    # Database table name
    __tablename__ = "shelves"

    # Unique identifier for each shelf
    id: Mapped[int] = mapped_column(primary_key=True)

    # Name of the shelf
    name: Mapped[str] = mapped_column(String(100))

    # Date and time when the shelf was created
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    # Reference to the owner of the shelf
    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
    )

    # Relationship with the User model
    owner: Mapped["User"] = relationship(
        "User",
        back_populates="shelves",
    )

    # Many-to-many relationship with books
    books: Mapped[list["Book"]] = relationship(
        "Book",
        secondary=book_shelves,
        back_populates="shelves",
    )

    # Users who have access to this shelf
    shares: Mapped[list["ShelfShare"]] = relationship(
    "ShelfShare",
    back_populates="shelf",
    cascade="all, delete-orphan",
    )