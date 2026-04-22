from datetime import date, datetime
from decimal import Decimal
from pydantic import BaseModel, Field


class ExpenseCreate(BaseModel):
    amount: Decimal = Field(..., gt=0)
    category: str = Field(..., min_length=1)
    description: str | None = Field(default=None, max_length=500)
    date: date


class ExpenseResponse(BaseModel):
    id: int
    amount: Decimal
    category: str
    description: str | None
    date: date
    created_at: datetime

    class Config:
        from_attributes = True