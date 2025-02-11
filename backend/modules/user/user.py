import uuid
from typing import Optional

from core.domain.domain_base import BaseDomain


class User(BaseDomain):
    """Domain Model: Represents a User in the system (DDD-compliant, ORM-agnostic)."""

    def __init__(
        self,
        email: str,
        hashed_password: str,
        user_name: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        has_agreed_terms: bool = False,
        **kwargs,  # Allows metadata fields (created_at, updated_at, etc.)
    ):
        super().__init__(**kwargs)  # Initialize metadata fields

        if not email or "@" not in email:
            raise ValueError("Invalid email format")
        if not has_agreed_terms:
            raise ValueError("User must agree to terms and conditions")

        self.email = email
        self.hashed_password = hashed_password
        self.user_name = user_name
        self.first_name = first_name
        self.last_name = last_name
        self.status = "active"
        self.is_email_verified = False
        self.verification_token = uuid.uuid4()
        self.has_agreed_terms = has_agreed_terms

    @classmethod
    def register_user(cls, email: str, hashed_password: str, has_agreed_terms: bool):
        """Factory method to enforce domain logic when creating a user."""
        return cls(email=email, hashed_password=hashed_password, has_agreed_terms=has_agreed_terms)

    def verify_email(self):
        """Marks the email as verified and removes the verification token."""
        self.is_email_verified = True
        self.verification_token = None

    def change_status(self, new_status: str):
        """Updates the user's status."""
        allowed_statuses = {"active", "inactive", "banned"}
        if new_status not in allowed_statuses:
            raise ValueError(f"Invalid status: {new_status}")
        self.status = new_status

    def update_profile(self, user_name: Optional[str] = None, first_name: Optional[str] = None,
                       last_name: Optional[str] = None):
        """Updates user profile information."""
        if user_name:
            self.user_name = user_name
        if first_name:
            self.first_name = first_name
        if last_name:
            self.last_name = last_name

    def __repr__(self) -> str:
        return f"User(id={self.id}, email={self.email}, status={self.status})"

