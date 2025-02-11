import enum

class MessageStatusEnum(enum.Enum):
    """Defines the possible statuses of an Outbox message."""
    PENDING = "PENDING"
    SENT = "SENT"
    FAILED = "FAILED"
