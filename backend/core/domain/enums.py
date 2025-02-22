from enum import Enum

class UserStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    BANNED = "banned"

class Role(Enum):
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"
