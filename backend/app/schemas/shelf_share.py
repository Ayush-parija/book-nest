from pydantic import BaseModel, ConfigDict, EmailStr

from app.models.share_role import ShelfRole


class ShelfShareCreate(BaseModel):
    email: EmailStr
    role: ShelfRole


class ShelfShareUpdate(BaseModel):
    role: ShelfRole


class ShelfCollaboratorResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: ShelfRole

    model_config = ConfigDict(
        from_attributes=True,
    )


class SharedShelfResponse(BaseModel):
    id: int
    name: str
    owner_name: str
    role: ShelfRole
    
    model_config = ConfigDict(
        from_attributes=True,
    )