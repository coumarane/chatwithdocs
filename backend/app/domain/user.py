from sqlalchemy.orm import Mapped, mapped_column
from app.domain.base_entity import BaseEntity

class User(BaseEntity):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)

    def __repr__(self) -> str:
        return f"User(id={self.id}, username={self.username}, email={self.email})"
