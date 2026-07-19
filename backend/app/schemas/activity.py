from datetime import datetime

from pydantic import BaseModel, ConfigDict


# Response schema for activity details
class ActivityResponse(BaseModel):
    # Unique activity ID
    id: int

    # ID of the user who performed the activity
    user_id: int

    # Type of activity
    action: str

    # Description of the activity
    message: str

    # Time when the activity was created
    created_at: datetime

    # Enable reading data directly from ORM models
    model_config = ConfigDict(from_attributes=True)