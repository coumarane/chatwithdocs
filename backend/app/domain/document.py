from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, Integer, UUID, ForeignKey, BigInteger, CheckConstraint
from app.domain.base_entity import BaseEntity
import uuid

# Documents Table
class Document(BaseEntity):
    __tablename__ = 'documents'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    file_name: Mapped[str] = mapped_column(String(255), nullable=False)
    file_path: Mapped[str] = mapped_column(Text, nullable=False)
    file_size: Mapped[int] = mapped_column(BigInteger, nullable=False)
    file_type: Mapped[str] = mapped_column(String(50), nullable=True)  # File format (e.g., pdf, docx, txt)
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)  # Versioning for document updates
    status: Mapped[str] = mapped_column(String(50), nullable=False, default='uploaded')  # Detailed status tracking
    failure_reason: Mapped[str] = mapped_column(Text, nullable=True)  # Error details if processing fails

    __table_args__ = (CheckConstraint('file_size > 0', name='chk_file_size'),)

    def __repr__(self) -> str:
        return f"Document(id={self.id}, user_id={self.user_id}, file_name={self.file_name}, file_size={self.file_size}, file_type={self.file_type}, status={self.status})"
