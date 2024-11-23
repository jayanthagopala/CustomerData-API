from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the FastAPI Customer API"}


def test_create_customer():
    response = client.post(
        "/customers/", json={"id": 1, "name": "John Doe", "email": "john@example.com"}
    )
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "John Doe", "email": "john@example.com"}


def test_get_customer():
    response = client.get("/customers/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "John Doe", "email": "john@example.com"}
