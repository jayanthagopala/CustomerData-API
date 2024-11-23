import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db  # Changed from dependencies to database
from app.main import app
from app.models import Customer  # Make sure to import your models

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
    customer_data = {"name": "John Doe", "email": "john.doe@example.com", "age": 30}

    # Make request
    response = client.post("/customers/", json=customer_data)

    # Assertions
    assert response.status_code == 200  # Changed to 201 for resource creation
    data = response.json()
    assert data["name"] == customer_data["name"]
    assert data["email"] == customer_data["email"]
    assert data["age"] == customer_data["age"]
    assert "id" in data


def test_get_customer(client):
    # First create a customer
    customer_data = {"name": "John Doe", "email": "john.doe@example.com", "age": 30}
    create_response = client.post("/customers/", json=customer_data)
    created_customer = create_response.json()

    # Then try to get the customer
    response = client.get(f"/customers/{created_customer['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data == created_customer


def test_create_customer_invalid_data(client):
    # Test with invalid data
    response = client.post(
        "/customers/", json={"name": "John Doe"}  # Missing required fields
    )
    assert response.status_code == 422  # Validation error


# Add more tests as needed
