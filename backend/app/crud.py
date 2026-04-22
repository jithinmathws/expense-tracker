from __future__ import annotations

import hashlib
from decimal import Decimal
from sqlalchemy.orm import Session

from . import models, schemas


def normalize_text(value: str | None) -> str:
    if value is None:
        return ""
    return value.strip()


def build_dedupe_key(expense: schemas.ExpenseCreate) -> str:
    normalized_category = normalize_text(expense.category).lower()
    normalized_description = normalize_text(expense.description)

    raw_key = "|".join(
        [
            str(expense.amount.quantize(Decimal("0.01"))),
            normalized_category,
            normalized_description,
            expense.date.isoformat(),
        ]
    )
    return hashlib.sha256(raw_key.encode("utf-8")).hexdigest()


def create_expense(db: Session, expense: schemas.ExpenseCreate) -> models.Expense:
    dedupe_key = build_dedupe_key(expense)

    existing_expense = (
        db.query(models.Expense)
        .filter(models.Expense.dedupe_key == dedupe_key)
        .first()
    )
    if existing_expense:
        return existing_expense

    db_expense = models.Expense(
        amount=str(expense.amount.quantize(Decimal("0.01"))),
        category=normalize_text(expense.category),
        description=normalize_text(expense.description) or None,
        date=expense.date,
        dedupe_key=dedupe_key,
    )

    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense


def get_expenses(
    db: Session,
    category: str | None = None,
    sort: str | None = None,
) -> list[models.Expense]:
    query = db.query(models.Expense)

    if category:
        query = query.filter(models.Expense.category == category.strip())

    if sort == "date_desc":
        query = query.order_by(models.Expense.date.desc(), models.Expense.created_at.desc())
    else:
        query = query.order_by(models.Expense.created_at.desc())

    return query.all()