import enum


# Enum representing the access levels for a shared shelf
class ShelfRole(str, enum.Enum):
    # Full control over the shelf
    OWNER = "owner"

    # Can modify the shelf and its books
    EDITOR = "editor"

    # Can only view the shelf
    VIEWER = "viewer"