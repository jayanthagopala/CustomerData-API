# FastAPI Customer API

A RESTful API built with FastAPI that manages customer information, allowing you to create and retrieve customer details.

## Features

- ✨ Modern FastAPI framework
- 🔐 Input validation using Pydantic models
- 📦 Poetry for dependency management
- 🗄️ SQLAlchemy ORM for database operations
- 📝 OpenAPI documentation (Swagger UI)
- 🔄 Automatic API documentation
- ✅ Type checking with Python type hints

## Technical Requirements

- Python 3.11+
- Poetry for dependency management
- PostgreSQL (or your preferred database)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/fastapi-customer-api.git
   cd fastapi-customer-api
   ```

2. Install Poetry (if not already installed):
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

3. Install dependencies:
   ```bash
   poetry install
   ```

4. Create a `.env` file in the project root:
   ```env
   DATABASE_URL=postgresql://user:password@localhost:5432/customer_db
   API_VERSION=v1
   ENVIRONMENT=development
   ```

## Running the Application

1. Activate the virtual environment:
   ```bash
   poetry shell
   ```

2. Start the FastAPI server:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

3. Access the API documentation:
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## API Documentation

### Customer Endpoints

#### Create Customer
- **URL**: `/api/v1/customers`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "first_name": "John",
    "last_name": "Doe",
    "date_of_birth": "1990-01-01"
  }
  ```
- **Success Response** (201 Created):
  ```json
  {
    "id": 1,
    "first_name": "John",
    "last_name": "Doe",
    "date_of_birth": "1990-01-01",
    "created_at": "2024-11-22T10:30:00Z"
  }
  ```

#### Get Customer
- **URL**: `/api/v1/customers/{customer_id}`
- **Method**: `GET`
- **URL Parameters**: `customer_id=[integer]`
- **Success Response** (200 OK):
  ```json
  {
    "id": 1,
    "first_name": "John",
    "last_name": "Doe",
    "date_of_birth": "1990-01-01",
    "created_at": "2024-11-22T10:30:00Z"
  }
  ```
- **Error Response** (404 Not Found):
  ```json
  {
    "detail": "Customer not found"
  }
  ```

## Project Structure
```
fastapi-customer-api/
├── app/
│   ├── api/
│   │   └── v1/
│   │       └── endpoints/
│   │           └── customers.py
│   ├── core/
│   │   ├── config.py
│   │   └── database.py
│   ├── models/
│   │   └── customer.py
│   ├── schemas/
│   │   └── customer.py
│   └── main.py
├── tests/
│   └── test_customers.py
├── .env
├── .gitignore
├── poetry.lock
├── pyproject.toml
└── README.md
```

## Development

### Running Tests
```bash
poetry run pytest
```

### Code Formatting
```bash
poetry run black .
poetry run isort .
```

### Type Checking
```bash
poetry run mypy .
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support, please open an issue in the GitHub repository or contact the maintainers.