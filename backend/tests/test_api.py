from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)


def test_create_expense():
    payload = {
        "amount": 100.50,
        "category": "Food",
        "description": "Lunch",
        "date": "2026-04-22",
    }

    response = client.post("/expenses", json=payload)

    assert response.status_code == 200
    data = response.json()

    assert data["amount"] == "100.50"
    assert data["category"] == "Food"
    assert data["description"] == "Lunch"
    assert data["date"] == "2026-04-22"


def test_duplicate_expense_prevention():
    payload = {
        "amount": 200,
        "category": "Travel",
        "description": "Taxi",
        "date": "2026-04-22",
    }

    response1 = client.post("/expenses", json=payload)
    response2 = client.post("/expenses", json=payload)

    assert response1.status_code == 200
    assert response2.status_code == 200

    data1 = response1.json()
    data2 = response2.json()

    # Same ID means duplicate was NOT created
    assert data1["id"] == data2["id"]