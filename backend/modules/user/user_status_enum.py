import enum

class UserStatusEnum(enum.Enum):
    """User status options."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    BANNED = "banned"
