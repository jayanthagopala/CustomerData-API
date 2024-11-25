import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app
from app.models import Customer

# Test database URL
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

# Create test engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# Create test session
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Override the get_db dependency
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


# Set up the dependency override
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function")
def test_db():
    # Create tables
    Base.metadata.create_all(bind=engine)
    yield  # Run the test
    # Drop tables after each test
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(test_db):
    # Return TestClient with fresh database
    with TestClient(app) as test_client:
        yield test_client


def test_create_customer(client):
    # Test data
    customer_data = {
        "first_name": "John",
        "last_name": "Doe",
        "date_of_birth": "1990-01-01",
    }

    # Make request
    response = client.post("/customers/", json=customer_data)

    # Assertions
    assert response.status_code == 201  # Resource created
    data = response.json()
    assert data["first_name"] == customer_data["first_name"]
    assert data["last_name"] == customer_data["last_name"]
    assert data["date_of_birth"] == customer_data["date_of_birth"]
    assert "id" in data


def test_get_customer(client):
    # First create a customer
    customer_data = {
        "first_name": "John",
        "last_name": "Doe",
        "date_of_birth": "1990-01-01",
    }
    create_response = client.post("/customers/", json=customer_data)
    created_customer = create_response.json()

    # Then try to get the customer
    response = client.get(f"/customers/{created_customer['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data == created_customer


def test_create_customer_invalid_data(client):
    # Test with invalid data (missing fields)
    response = client.post("/customers/", json={"first_name": "John"})
    assert response.status_code == 422  # Validation error


def test_update_customer(client):
    # Create a customer
    customer_data = {
        "first_name": "John",
        "last_name": "Doe",
        "date_of_birth": "1990-01-01",
    }
    create_response = client.post("/customers/", json=customer_data)
    customer_id = create_response.json()["id"]

    # Update the customer
    update_data = {"first_name": "Johnny"}
    response = client.put(f"/customers/{customer_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == "Johnny"
    assert data["last_name"] == customer_data["last_name"]
    assert data["date_of_birth"] == customer_data["date_of_birth"]


def test_delete_customer(client):
    # Create a customer
    customer_data = {
        "first_name": "John",
        "last_name": "Doe",
        "date_of_birth": "1990-01-01",
    }
    create_response = client.post("/customers/", json=customer_data)
    customer_id = create_response.json()["id"]

    # Delete the customer
    delete_response = client.delete(f"/customers/{customer_id}")
    assert delete_response.status_code == 200
    assert delete_response.json() == {"message": "Customer deleted successfully"}


def test_get_customers_pagination(client):
    # Create sample customers
    for i in range(15):
        client.post(
            "/customers/",
            json={
                "first_name": f"Customer{i}",
                "last_name": "Test",
                "date_of_birth": f"199{i}-01-01",
            },
        )

    # Test pagination
    response = client.get("/customers/?skip=0&limit=5")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5
    assert all(isinstance(customer, dict) for customer in data)
    assert [customer["first_name"] for customer in data] == [
        f"Customer{i}" for i in range(5)
    ]
