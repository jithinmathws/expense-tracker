from __future__ import annotations

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from . import crud, schemas
from .database import Base, SessionLocal, engine

app = FastAPI(title="Expense Tracker API")

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "Expense Tracker API"}


@app.post("/expenses", response_model=schemas.ExpenseResponse)
def create_expense(
    expense: schemas.ExpenseCreate,
    db: Session = Depends(get_db),
):
    return crud.create_expense(db, expense)


@app.get("/expenses", response_model=list[schemas.ExpenseResponse])
def list_expenses(
    category: str | None = None,
    sort: str | None = None,
    db: Session = Depends(get_db),
):
    return crud.get_expenses(db, category=category, sort=sort)