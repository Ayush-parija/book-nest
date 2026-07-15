from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str]
    email: Mapped[str]
    password_hash: Mapped[str]

    books: Mapped[list["Book"]] = relationship(
        "Book",
        back_populates="owner",
        cascade="all, delete-orphan",
    )

    shelves: Mapped[list["Shelf"]] = relationship(
        "Shelf",
        back_populates="owner",
        cascade="all, delete-orphan",
    )