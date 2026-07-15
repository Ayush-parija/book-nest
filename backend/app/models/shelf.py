from datetime import datetime

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

from app.db.database import Base


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


class Shelf(Base):
    __tablename__ = "shelves"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(100))

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
    )

    owner: Mapped["User"] = relationship(
        "User",
        back_populates="shelves",
    )

    books: Mapped[list["Book"]] = relationship(
        "Book",
        secondary=book_shelves,
        back_populates="shelves",
    )