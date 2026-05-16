# Expense Tracker

## Overview

This project is a lightweight backend-focused expense tracking system built with FastAPI and SQLite. The primary engineering focus was correctness, maintainability, and predictable behavior under real-world operational conditions such as retries, duplicate submissions, and unstable network behavior.

The system exposes RESTful APIs for expense creation and retrieval while ensuring retry-safe behavior through deterministic request deduplication. The implementation intentionally prioritizes simplicity, clear separation of concerns, and reliability over unnecessary complexity.

The application consists of:

* A FastAPI backend responsible for API logic, validation, persistence, and retry-safe request handling
* A lightweight Streamlit frontend used for interacting with the backend APIs

---

## Live Demo

Frontend: https://expense-tracker-ui.streamlit.app/
Backend API: https://expense-tracker-api-mz99.onrender.com/
Backend Docs: https://expense-tracker-api-mz99.onrender.com/docs

---

## Features

* Create a new expense (amount, category, description, date)
* View a list of expenses
* Filter expenses by category
* Sort expenses by date (newest first)
* View total amount for the currently visible expenses
* Retry-safe expense creation (prevents duplicate entries)

---

## Tech Stack

* **Backend:** FastAPI
* **Frontend:** Streamlit
* **Database:** SQLite
* **Data Handling:** Python `Decimal` for accurate monetary calculations

---

## Engineering Focus

The project was designed around a few core engineering goals:

* Deterministic and retry-safe API behavior
* Clear separation between frontend and backend responsibilities
* Maintainable and testable backend code
* Explicit handling of operational edge cases
* Simplicity and readability over unnecessary abstraction

Particular attention was given to ensuring the system behaves correctly under duplicate submissions and unstable network conditions, which are common sources of subtle production bugs in real-world systems.

---

## Key Design Decisions

### Retry-safe Expense Creation

The `POST /expenses` endpoint is designed to handle duplicate submissions caused by retries, page refreshes, or slow network conditions.

A deduplication key is generated based on:

* amount
* category
* description
* date

This key is stored with a unique constraint, ensuring that repeated submissions of the same expense do not create duplicate records. Instead, the existing record is returned.
This approach was chosen to simulate idempotency behavior commonly used in production systems where retries, refreshes, or transient failures can otherwise create inconsistent state.

---

### Money Handling with Decimal

Expense amounts are handled using Python's `Decimal` type instead of floating-point numbers to avoid precision errors in financial calculations.

---

### Persistence with SQLite

SQLite was chosen as a lightweight persistence layer:

* No external setup required
* Suitable for small-scale applications
* Enables realistic data storage within time constraints

---

### Backend and Frontend Separation

The system is structured with:

* a FastAPI backend responsible for API logic and data handling
* a Streamlit frontend responsible for user interaction

This separation improves clarity and makes the system easier to extend or replace components in the future.

---

## System Architecture

```
Streamlit Frontend
        │
        ▼
FastAPI Backend
        │
        ▼
SQLite Database
```

The frontend communicates with the backend exclusively through HTTP APIs. The backend is responsible for validation, deduplication logic, persistence, and business rules.

---

## Handling Real-World Conditions

The system is designed to behave correctly under realistic usage scenarios:

* **Duplicate submissions:** Prevented using a deduplication key
* **Page refresh after submit:** Does not create duplicate entries
* **Network retries:** Safe due to idempotent-like behavior of the POST endpoint
* **API failures:** Frontend displays appropriate error messages

---

## Testing

Basic API tests are included to verify:

* Expense creation
* Duplicate prevention (retry-safe behavior)

---

## Trade-offs

* SQLite was used instead of a production-grade database (e.g., PostgreSQL) to reduce setup complexity.
* Streamlit was chosen over a full frontend framework (e.g., React) for faster development and simplicity.
* No authentication or multi-user support was implemented to keep the scope focused on core functionality.
* Deployment configuration was kept minimal to prioritize working functionality within the time constraint.
* The architecture intentionally avoids unnecessary abstractions to keep the codebase easy to reason about and discuss in an interview setting.

---

## What Was Not Implemented

* User authentication and authorization
* Editing or deleting expenses
* Advanced filtering or search
* Production-grade deployment setup
* Extensive automated test coverage (only core API behavior is tested)

---

## Running the Project

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Backend will run at:

```
http://127.0.0.1:8000
```

---

### Frontend

```bash
cd frontend
pip install -r requirements.txt
streamlit run app.py
```

* Ensure the backend is running before starting the frontend.

---

## Future Improvements

* Replacing SQLite with PostgreSQL
* Introducing async database access patterns
* Adding structured logging and observability
* Implementing authentication and multi-user isolation
* Adding stronger automated test coverage
* Introducing background job processing for asynchronous workflows
* Adding metrics and monitoring for operational visibility

---

## Deployment Notes

The application is deployed as two separate services:

* The FastAPI backend is deployed on Render
* The Streamlit frontend is deployed on Streamlit Community Cloud

The frontend communicates with the backend via HTTP requests.

Note: SQLite is used for persistence. On some hosting platforms, the filesystem may be ephemeral, so data may not persist across restarts. In a production system, this would be replaced with a managed database such as PostgreSQL.

---

## Notes

The frontend is currently configured to call the backend at:

```
http://127.0.0.1:8000
```

In a production setup, this would be made configurable using environment variables.

---
