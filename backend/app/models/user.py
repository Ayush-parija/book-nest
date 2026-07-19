from sqlalchemy.orm import Mapped, mapped_column, relationship

# Base class for all database models
from app.db.database import Base

# Model for shared shelf access
from app.models.shelf_share import ShelfShare


# User model
class User(Base):
    # Database table name
    __tablename__ = "users"

    # Unique identifier for each user
    id: Mapped[int] = mapped_column(primary_key=True)

    # User's full name
    name: Mapped[str]

    # User's email address
    email: Mapped[str]

    # Hashed password for authentication
    password_hash: Mapped[str]

    # Books owned by the user
    books: Mapped[list["Book"]] = relationship(
        "Book",
        back_populates="owner",
        cascade="all, delete-orphan",
    )

    # Shelves created by the user
    shelves: Mapped[list["Shelf"]] = relationship(
        "Shelf",
        back_populates="owner",
        cascade="all, delete-orphan",
    )

    # Shelves shared with the user
    shared_shelves: Mapped[list["ShelfShare"]] = relationship(
    "ShelfShare",
    back_populates="user",
    cascade="all, delete-orphan",
    )

    # Activity history of the user
    activities: Mapped[list["Activity"]] = relationship(
    "Activity",
    back_populates="user",
    cascade="all, delete-orphan",
)