from enum import Enum

class DocumentStatus(str, Enum):
    """Represents possible statuses of a Document in the domain."""
    UPLOADED = "UPLOADED"
    VECTORIZED = "VECTORIZED"
    READY = "READY"
    ERROR = "ERROR"
