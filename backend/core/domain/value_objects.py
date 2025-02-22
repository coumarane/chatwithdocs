import re


class Email:
    """Encapsulates an Email Address with Validation."""

    def __init__(self, address: str):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", address):
            raise ValueError("Invalid email format")
        self.address = address

    def __str__(self):
        return self.address

    def __eq__(self, other):
        return isinstance(other, Email) and self.address == other.address
