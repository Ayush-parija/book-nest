from datetime import datetime

from pydantic import BaseModel, ConfigDict


# Request schema for creating a new shelf
class ShelfCreate(BaseModel):
    # Name of the shelf
    name: str


# Request schema for updating shelf details
class ShelfUpdate(BaseModel):
    # Updated shelf name
    name: str | None = None


# Response schema for shelf information
class ShelfResponse(BaseModel):
    # Unique shelf ID
    id: int

    # Shelf name
    name: str

    # ID of the shelf owner
    owner_id: int

    # Date and time when the shelf was created
    created_at: datetime

    # Enable conversion from SQLAlchemy models
    model_config = ConfigDict(
        from_attributes=True,
    )