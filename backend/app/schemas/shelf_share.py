from pydantic import BaseModel, ConfigDict, EmailStr

# Enum representing shelf access roles
from app.models.share_role import ShelfRole


# Request schema for sharing a shelf with a user
class ShelfShareCreate(BaseModel):
    # Email of the user to share the shelf with
    email: EmailStr

    # Access level assigned to the user
    role: ShelfRole


# Request schema for updating a collaborator's role
class ShelfShareUpdate(BaseModel):
    # Updated access level
    role: ShelfRole


# Response schema for collaborator details
class ShelfCollaboratorResponse(BaseModel):
    # User ID
    id: int

    # Collaborator name
    name: str

    # Collaborator email
    email: EmailStr

    # Assigned role
    role: ShelfRole

    # Enable conversion from SQLAlchemy models
    model_config = ConfigDict(
        from_attributes=True,
    )


# Response schema for shared shelf information
class SharedShelfResponse(BaseModel):
    # Shelf ID
    id: int

    # Shelf name
    name: str

    # Name of the shelf owner
    owner_name: str

    # User's role in the shared shelf
    role: ShelfRole

    # Enable conversion from SQLAlchemy models
    model_config = ConfigDict(
        from_attributes=True,
    )