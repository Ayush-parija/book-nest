from sqlalchemy import Enum, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base
from app.models.share_role import ShelfRole


class ShelfShare(Base):
    __tablename__ = "shelf_shares"

    __table_args__ = (
        UniqueConstraint(
            "shelf_id",
            "user_id",
            name="uq_shelf_user",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    shelf_id: Mapped[int] = mapped_column(
        ForeignKey(
            "shelves.id",
            ondelete="CASCADE",
        )
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        )
    )

    role: Mapped[ShelfRole] = mapped_column(
        Enum(ShelfRole),
        default=ShelfRole.VIEWER,
    )

    shelf = relationship(
        "Shelf",
        back_populates="shares",
    )

    user = relationship(
        "User",
        back_populates="shared_shelves",
    )