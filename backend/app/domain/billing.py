from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DECIMAL, TIMESTAMP, UUID, ForeignKey
from app.domain.base_entity import BaseEntity
import uuid

# Billing Table
class Billing(BaseEntity):
    __tablename__ = 'billings'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    subscription_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('subscriptions.id', ondelete='CASCADE'), nullable=False)
    amount: Mapped[float] = mapped_column(DECIMAL(10, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(10), nullable=False, default='USD')
    payment_status: Mapped[str] = mapped_column(String(50), nullable=False, default='pending')  # Pending, Paid, Failed
    payment_date: Mapped[str] = mapped_column(TIMESTAMP, nullable=True)

    def __repr__(self) -> str:
        return f"Billing(id={self.id}, user_id={self.user_id}, subscription_id={self.subscription_id}, amount={self.amount}, currency={self.currency}, payment_status={self.payment_status})"

