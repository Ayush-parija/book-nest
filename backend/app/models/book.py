from datetime import datetime
import enum

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base
from app.models.shelf import book_shelves

from sqlalchemy import Boolean


class BookStatus(str, enum.Enum):
    WANT_TO_READ = "Want to Read"
    READING = "Reading"
    FINISHED = "Finished"


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)

    title: Mapped[str] = mapped_column(String(255))

    author: Mapped[str] = mapped_column(String(255))

    status: Mapped[BookStatus] = mapped_column(
        Enum(BookStatus),
        default=BookStatus.WANT_TO_READ,
    )

    total_pages: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    current_page: Mapped[int | None] = mapped_column(
        Integer,
        default=0,
        nullable=True,
    )

    rating: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    finished_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
    )

    # Relationship with User
    owner: Mapped["User"] = relationship(
        "User",
        back_populates="books",
    )

    # Many-to-Many Relationship with Shelf
    shelves: Mapped[list["Shelf"]] = relationship(
        "Shelf",
        secondary=book_shelves,
        back_populates="books",
    )

    is_favorite: Mapped[bool] = mapped_column(
    Boolean,
    default=False,)