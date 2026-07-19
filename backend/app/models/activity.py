from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

# Base class for all database models
from app.db.database import Base


# Activity model for storing user actions
class Activity(Base):
    # Database table name
    __tablename__ = "activities"

    # Unique identifier for each activity
    id = Column(Integer, primary_key=True, index=True)

    # Reference to the user who performed the activity
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    # Type of activity performed
    action = Column(
        String,
        nullable=False,
    )

    # Detailed activity message
    message = Column(
        String,
        nullable=False,
    )

    # Timestamp when the activity was created
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    # Relationship with the User model
    user = relationship(
        "User",
        back_populates="activities",
    )