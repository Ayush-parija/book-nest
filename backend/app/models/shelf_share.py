from sqlalchemy import Enum, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

# Base class for all database models
from app.db.database import Base

# Enum defining the access roles for shared shelves
from app.models.share_role import ShelfRole


# Model for managing shelf sharing between users
class ShelfShare(Base):
    # Database table name
    __tablename__ = "shelf_shares"

    # Ensure a user can be added only once to the same shelf
    __table_args__ = (
        UniqueConstraint(
            "shelf_id",
            "user_id",
            name="uq_shelf_user",
        ),
    )

    # Unique identifier for each shared record
    id: Mapped[int] = mapped_column(primary_key=True)

    # Reference to the shared shelf
    shelf_id: Mapped[int] = mapped_column(
        ForeignKey(
            "shelves.id",
            ondelete="CASCADE",
        )
    )

    # Reference to the user with whom the shelf is shared
    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        )
    )

    # Permission assigned to the user
    role: Mapped[ShelfRole] = mapped_column(
        Enum(ShelfRole),
        default=ShelfRole.VIEWER,
    )

    # Relationship with the Shelf model
    shelf = relationship(
        "Shelf",
        back_populates="shares",
    )

    # Relationship with the User model
    user = relationship(
        "User",
        back_populates="shared_shelves",
    )