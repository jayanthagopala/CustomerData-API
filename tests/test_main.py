import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
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


def test_delete_nonexistent_customer(client):
    # Attempt to delete a customer that doesn't exist
    response = client.delete("/customers/999")  # Non-existent ID

    # Assertions
    assert response.status_code == 404  # Not Found
    data = response.json()
    assert data["detail"] == "Customer with ID 999 not found."


def test_delete_existing_customer(client):
    # Create a customer
    customer = {"name": "John Doe", "email": "john.doe@example.com", "age": 30}
    create_response = client.post("/customers/", json=customer)
    assert create_response.status_code == 200
    customer_id = create_response.json()["id"]

    # Delete the customer
    delete_response = client.delete(f"/customers/{customer_id}")
    assert delete_response.status_code == 200
    assert delete_response.json() == {"message": "Customer deleted successfully"}


def test_double_deletion(client):
    # Create a customer
    customer = {"name": "John Doe", "email": "john.doe@example.com", "age": 30}
    create_response = client.post("/customers/", json=customer)
    assert create_response.status_code == 200
    customer_id = create_response.json()["id"]

    # Delete the customer
    delete_response = client.delete(f"/customers/{customer_id}")
    assert delete_response.status_code == 200

    # Try to delete the same customer again
    delete_response = client.delete(f"/customers/{customer_id}")
    assert delete_response.status_code == 404
    assert (
        delete_response.json()["detail"] == f"Customer with ID {customer_id} not found."
    )


def test_update_customer_duplicate_email(client):
    # Create two customers
    customer1 = {"name": "John Doe", "email": "john.doe@example.com", "age": 30}
    customer2 = {"name": "Jane Doe", "email": "jane.doe@example.com", "age": 25}
    client.post("/customers/", json=customer1)
    client.post("/customers/", json=customer2)

    # Attempt to update the second customer's email to the first customer's email
    response = client.put("/customers/2", json={"email": "john.doe@example.com"})
    assert response.status_code == 400
    assert response.json()["detail"] == "A customer with this email already exists."


@pytest.fixture(scope="function")
def sample_customers(client):
    """
    Create sample customers for testing pagination.
    Returns the client fixture after creating the test data.
    """
    # Create 15 sample customers
    for i in range(15):
        response = client.post(
            "/customers/",
            json={
                "name": f"Customer {i}",
                "email": f"customer{i}@example.com",
                "age": 20 + i,
            },
        )
        assert (
            response.status_code == 200
        )  # Verify each customer is created successfully

    return client


def test_get_customers_pagination(sample_customers):
    """
    Test pagination with `skip` and `limit` parameters.
    """
    client = sample_customers  # Get the client with pre-populated data

    # Test case 1: First page (5 customers)
    response = client.get("/customers/?skip=0&limit=5")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5
    assert all(isinstance(customer, dict) for customer in data)
    assert [customer["name"] for customer in data] == [
        f"Customer {i}" for i in range(5)
    ]

    # Test case 2: Second page (5 customers)
    response = client.get("/customers/?skip=5&limit=5")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5
    assert [customer["name"] for customer in data] == [
        f"Customer {i}" for i in range(5, 10)
    ]

    # Test case 3: Last page (partial)
    response = client.get("/customers/?skip=10&limit=5")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5
    assert [customer["name"] for customer in data] == [
        f"Customer {i}" for i in range(10, 15)
    ]

    # Test case 4: Beyond available data
    response = client.get("/customers/?skip=15&limit=5")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0
    assert isinstance(data, list)


def test_get_customers_default_pagination(sample_customers):
    """
    Test default pagination when no parameters are provided.
    """
    client = sample_customers

    # Test default pagination (should return first 10 customers)
    response = client.get("/customers/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 10  # Default limit should be 10
    assert [customer["name"] for customer in data] == [
        f"Customer {i}" for i in range(10)
    ]


def test_get_customers_invalid_pagination(sample_customers):
    """
    Test invalid pagination parameters.
    """
    client = sample_customers

    # Test case 1: Negative skip
    response = client.get("/customers/?skip=-5&limit=5")
    assert response.status_code == 400
    error_detail = response.json()["detail"]
    assert (
        "Invalid pagination parameters. 'skip' must be >= 0 and 'limit' must be >= 1."
        in error_detail
    )

    # Test case 2: Negative limit
    response = client.get("/customers/?skip=0&limit=-5")
    assert response.status_code == 400
    error_detail = response.json()["detail"]
    assert (
        "Invalid pagination parameters. 'skip' must be >= 0 and 'limit' must be >= 1."
        in error_detail
    )

    # Test case 3: Zero limit
    response = client.get("/customers/?skip=0&limit=0")
    assert response.status_code == 400
    error_detail = response.json()["detail"]
    assert (
        "Invalid pagination parameters. 'skip' must be >= 0 and 'limit' must be >= 1."
        in error_detail
    )

    # Test case 4: Extremely large limit
    response = client.get("/customers/?skip=0&limit=1001")
    assert response.status_code == 400
    error_detail = response.json()["detail"]
    assert (
        "Invalid pagination parameters. 'skip' must be >= 0 and 'limit' must be >= 1."
        in error_detail
    )


def test_get_customers_edge_cases(sample_customers):
    """
    Test edge cases for pagination.
    """
    client = sample_customers

    # Test case 1: Skip equals total records
    response = client.get("/customers/?skip=15&limit=10")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0

    # Test case 2: High skip with small limit
    response = client.get("/customers/?skip=13&limit=5")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2  # Should only return the last 2 customers
    assert [customer["name"] for customer in data] == ["Customer 13", "Customer 14"]

    # Test case 3: Exact limit to end of data
    response = client.get("/customers/?skip=10&limit=5")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5
    assert [customer["name"] for customer in data] == [
        f"Customer {i}" for i in range(10, 15)
    ]
