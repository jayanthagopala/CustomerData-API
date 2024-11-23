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


def test_create_customer_missing_email(client):
    # Test data with missing email
    customer_data = {"name": "John Doe", "age": 30}

    # Make request
    response = client.post("/customers/", json=customer_data)

    # Assertions
    assert response.status_code == 422  # Validation error
    data = response.json()
    assert (
        data["detail"]
        == "Request validation failed. Ensure all required fields are included."
    )


def test_create_customer_missing_name(client):
    # Test data with missing name
    customer_data = {"email": "john.doe@example.com", "age": 30}

    # Make request
    response = client.post("/customers/", json=customer_data)

    # Assertions
    assert response.status_code == 422  # Validation error
    data = response.json()
    assert (
        data["detail"]
        == "Request validation failed. Ensure all required fields are included."
    )


def test_create_customer_missing_age(client):
    # Test data with missing age
    customer_data = {"name": "John Doe", "email": "john.doe@example.com"}

    # Make request
    response = client.post("/customers/", json=customer_data)

    # Assertions
    assert response.status_code == 422  # Validation error
    data = response.json()
    assert (
        data["detail"]
        == "Request validation failed. Ensure all required fields are included."
    )


def test_create_customer_duplicate_email(client):
    # Create the first customer
    first_customer = {"name": "John Doe", "email": "john.doe@example.com", "age": 30}
    response = client.post("/customers/", json=first_customer)
    assert response.status_code == 200  # Customer created successfully

    # Attempt to create another customer with the same email
    duplicate_customer = {
        "name": "Jane Doe",
        "email": "john.doe@example.com",  # Same email as the first customer
        "age": 25,
    }
    response = client.post("/customers/", json=duplicate_customer)
    assert response.status_code == 400  # HTTPException for duplicate email
    assert response.json()["detail"] == "A customer with this email already exists."


def test_update_nonexistent_customer(client):
    # Attempt to update a customer that doesn't exist
    customer_update = {
        "name": "Updated Name",
        "email": "updated.email@example.com",
        "age": 35,
    }
    response = client.put("/customers/999", json=customer_update)  # Non-existent ID

    # Assertions
    assert response.status_code == 404  # Not Found
    data = response.json()
    assert data["detail"] == f"Customer with ID 999 not found."


def test_empty_update_request(client):
    # Create a customer to test updates
    customer = {"name": "John Doe", "email": "john.doe@example.com", "age": 30}
    create_response = client.post("/customers/", json=customer)
    assert create_response.status_code == 200  # Customer created successfully
    customer_id = create_response.json()["id"]

    # Attempt to update with an empty request body
    empty_update = {}
    update_response = client.put(f"/customers/{customer_id}", json=empty_update)

    # Assertions
    assert update_response.status_code == 400  # Bad Request
    assert (
        update_response.json()["detail"]
        == "At least one field must be provided for update."
    )
