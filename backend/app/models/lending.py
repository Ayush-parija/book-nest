from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from app.db.database import Base


class Lending(Base):
    __tablename__ = "lendings"

    id = Column(Integer, primary_key=True, index=True)

    book_id = Column(
        Integer,
        ForeignKey("books.id", ondelete="CASCADE"),
        nullable=False,
    )

    owner_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )

    borrower_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )

    lent_at = Column(
        DateTime,
        default=datetime.utcnow,
    )

    returned_at = Column(
        DateTime,
        nullable=True,
    )

    # Relationships
    book = relationship("Book")
    owner = relationship(
        "User",
        foreign_keys=[owner_id],
    )
    borrower = relationship(
        "User",
        foreign_keys=[borrower_id],
    )