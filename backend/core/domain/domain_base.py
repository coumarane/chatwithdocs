import uuid
import datetime
from typing import Optional

class BaseDomain:
    """Base class for all domain entities (ORM-independent)."""

    def __init__(
        self,
        id: Optional[uuid.UUID] = None,
        created_at: Optional[datetime.datetime] = None,
        updated_at: Optional[datetime.datetime] = None,
        user_created: Optional[str] = None,
        user_updated: Optional[str] = None,
    ):
        self.id = id or uuid.uuid4()
        self.created_at = created_at or datetime.datetime.utcnow()
        self.updated_at = updated_at or self.created_at
        self.user_created = user_created
        self.user_updated = user_updated

    def update_metadata(self, current_user: Optional[str] = None):
        """Updates metadata fields (used for auditing)."""
        self.updated_at = datetime.datetime.utcnow()
        self.user_updated = current_user

    def __eq__(self, other):
        """Defines equality check based on ID."""
        if isinstance(other, BaseDomain):
            return self.id == other.id
        return False

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id})"
