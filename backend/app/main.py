from fastapi import FastAPI
from .database import engine, Base

app = FastAPI()

# create tables
Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "Expense Tracker API"}