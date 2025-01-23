from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, DECIMAL, Integer, UUID, ForeignKey, Boolean, Date, \
    UniqueConstraint
from app.domain.base_entity import BaseEntity
import uuid

# Plans Table
class Plan(BaseEntity):
    __tablename__ = 'plans'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    price: Mapped[float] = mapped_column(DECIMAL(10, 2), nullable=False, default=0.0)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    max_documents: Mapped[int] = mapped_column(Integer, nullable=True)
    max_storage: Mapped[float] = mapped_column(DECIMAL(10, 2), nullable=True)  # in GB

    def __repr__(self) -> str:
        return f"Plan(id={self.id}, name={self.name}, price={self.price})"


# Plan_Features Table
class PlanFeature(BaseEntity):
    __tablename__ = 'plan_features'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    plan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('plans.id', ondelete='CASCADE'), nullable=False)
    feature_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('features.id', ondelete='CASCADE'), nullable=False)

    __table_args__ = (UniqueConstraint('plan_id', 'feature_id', name='uq_plan_feature'),)

    def __repr__(self) -> str:
        return f"PlanFeature(id={self.id}, plan_id={self.plan_id}, feature_id={self.feature_id})"


# Subscriptions Table
class Subscription(BaseEntity):
    __tablename__ = 'subscriptions'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    plan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('plans.id', ondelete='CASCADE'), nullable=False)
    start_date: Mapped[Date] = mapped_column(Date, nullable=False)
    end_date: Mapped[Date] = mapped_column(Date, nullable=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default='active')

    __table_args__ = (UniqueConstraint('user_id', 'plan_id', name='uq_user_plan'),)

    def __repr__(self) -> str:
        return f"Subscription(id={self.id}, user_id={self.user_id}, plan_id={self.plan_id}, status={self.status})"


# Trial_Periods Table
class TrialPeriod(BaseEntity):
    __tablename__ = 'trial_periods'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    start_date: Mapped[Date] = mapped_column(Date, nullable=False)
    end_date: Mapped[Date] = mapped_column(Date, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    def __repr__(self) -> str:
        return f"TrialPeriod(id={self.id}, user_id={self.user_id}, start_date={self.start_date}, end_date={self.end_date}, is_active={self.is_active})"
