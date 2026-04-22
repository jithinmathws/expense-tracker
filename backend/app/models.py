from sqlalchemy import Column, Integer, String, Date, DateTime, UniqueConstraint
from sqlalchemy.sql import func

from .database import Base


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(String, nullable=False)  # store Decimal as string
    category = Column(String, nullable=False)
    description = Column(String, nullable=True)
    date = Column(Date, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    dedupe_key = Column(String, nullable=False, unique=True)

    __table_args__ = (
        UniqueConstraint("dedupe_key", name="uq_expense_dedupe"),
    )