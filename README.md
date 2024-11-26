# Customer Data Management API

A Python-based project built with FastAPI, to manage customer data.

- Provides endpoints for creating, retrieving, updating, and deleting customer records.
- Supports filtering and pagination to ensure efficient and flexible data retrieval.

---

## 🛠️ **Endpoints Overview**

| Method | Endpoint | Description | Request Body (JSON) |
|--------|----------|-------------|---------------------|
| POST | /customers/ | Create a new customer | `{ "first_name": "string", "last_name": "string", "date_of_birth": "string (YYYY-MM-DD)" }` |
| GET | /customers/ | List customers with pagination support | N/A |
| GET | /customers/{id} | Retrieve a customer by ID | N/A |
| PUT | /customers/{id} | Update an existing customer by ID | `{ "first_name": "string", "last_name": "string", "date_of_birth": "string (YYYY-MM-DD)" }` |
| DELETE | /customers/{id} | Delete a customer by ID | N/A |
| GET | /customers/by-date-range?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD | Retrieve customers born between the specified start and end dates | N/A |
---
#### **Pagination Parameters for `GET /customers/`**
- **`skip`**: Number of records to skip (default: `0`).
- **`limit`**: Maximum number of records to return (default: `10`).

---

## **Features**

- **FastAPI Framework**:
  - Built on FastAPI
  - Provides built-in support for OpenAPI (Swagger UI) and ReDoc for interactive API documentation.

- **Automatic Data Validation with Pydantic**:
  - Ensures robust data validation for request and response payloads using Pydantic.
  - Supports complex data types, type annotations, and field validation with clear error messages.

- **Error Handling and Validation**:
  - Built-in error handling for invalid request data (e.g., malformed JSON, missing required fields).
  - Custom exception handling for meaningful error messages.

- **Pre-Commit Hooks for Code Quality**:
  - Automates code formatting and quality checks using pre-commit hooks.
  - Integrates tools like:
    - **Black**: Ensures consistent code formatting.
    - **Isort**: Automatically organizes imports.
    - **Ruff**: Lints code for syntax and styling issues.
    - **Trailing Whitespace Fixer**: Removes unnecessary whitespace.

- **Testing Suite**:
  - Comprehensive test cases for all endpoints using `pytest` and FastAPI's `TestClient`.
  - Includes edge case testing, performance testing, and error handling validation.

- **Environment Configuration**:
  - `.env` file support for managing sensitive configurations like database URLs and environment settings.
  - Separate configurations for development, testing, and production environments.

- **Pagination and Filtering**:
  - API supports pagination and filtering for endpoints that return lists of resources, ensuring efficient data handling.

- **API Documentation**:
  - Automatically generated interactive documentation via Swagger UI and ReDoc.
  - Clear, well-organized documentation for all endpoints, with detailed descriptions of input and output.

---

## 🛠️ **Project Setup**

### **1. Clone the Repository**
```bash
git clone <repository-url>
cd FastAPI-API
```

### **2. Create a Conda Environment**
```bash
conda config --set auto_activate_base false
conda create --name fastapi python=3.12
conda activate fastapi
```

### **3. Install Poetry**
Install Poetry using:
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Ensure Poetry is available in your path:
```bash
poetry --version
```

### **4. Install Dependencies**
```bash
poetry install
```

---

## 📂 **Project Structure**
```
FastAPI-API/
├── app/
│   ├── __init__.py            # Marks the `app` directory as a Python module
│   ├── main.py                # Entry point for the FastAPI application; defines the app and includes routes
│   ├── schemas.py             # Pydantic schemas for request/response validation and data modeling
│   ├── crud.py                # CRUD operations for interacting with the database (create, read, update, delete)
│   ├── models.py              # SQLAlchemy models representing the database tables
│   ├── database.py            # Database connection setup, including engine and session management
│   ├── routers/               # Contains route definitions for organizing API endpoints
│   │   ├── __init__.py        # Marks the `routers` directory as a Python module and aggregates all routers
│   │   ├── customers.py       # Routes related to customer data management (e.g., create, update, fetch, delete)
│   ├── utils/                 # Utility functions and helpers used across the application
│   │   ├── __init__.py        # Marks the `utils` directory as a Python module
│   │   ├── logger.py          # Custom logging setup for tracking application activity
├── tests/
│   ├── __init__.py            # Marks the `tests` directory as a Python module
│   ├── test_main.py           # Test cases for API endpoints and application logic
├── performance_tests/
│   ├── locustfile.py          # Locust-based performance and load testing scripts for the API
│   ├── README.md              # Documentation for running and understanding performance tests
├── .env                       # Environment variables file for managing sensitive configuration (e.g., database URL)
├── .pre-commit-config.yaml    # Configuration for pre-commit hooks to enforce code quality and styling checks
├── .gitignore                 # Specifies intentionally untracked files to ignore in version control
├── poetry.lock                # Dependency lock file generated by Poetry to ensure deterministic builds
├── pyproject.toml             # Poetry configuration file for dependencies and project settings
├── README.md                  # Main project documentation with setup instructions, features, and usage
└── postman/
    ├── FastAPI-API-Postman-Collection.json  # Pre-configured Postman collection for testing API endpoints
```

---

## 📋 **Environment Variables**
Create a `.env` file in the root directory to manage sensitive configurations:
```env
ENVIRONMENT=development
DATABASE_URL=sqlite:///./test.db
```

---

## 🖥️ **Running the Application**

### **Start the Server**
Run the development server using Uvicorn:
```bash
uvicorn app.main:app --reload
```

The server will be available at [http://localhost:8000](http://localhost:8000).

### **API Documentation**
- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 🔍 **Testing**

### **Run Tests**
Execute the tests using pytest:
```bash
pytest tests/
```

### **Linting and Formatting**
Pre-commit hooks ensure code quality:
- **Black**: Code formatting.
- **Isort**: Import sorting.
- **Ruff**: Linting.

Manually run all hooks:
```bash
pre-commit run --all-files
```

---

## 🛡️ **Pre-Commit Hooks**

This project uses `pre-commit` hooks to automate code quality checks. They are configured in `.pre-commit-config.yaml`. Install the hooks with:
```bash
pre-commit install
```

### Included Hooks:
- **Black**: Code formatter.
- **Isort**: Import organizer.
- **Ruff**: Linter for Python code.
- **Trailing Whitespace**: Removes trailing spaces.
- **End of File Fixer**: Ensures a single newline at the end of files.

---

## 📫 **Postman Collection**
A Postman collection is provided to test the API.

**Steps to Use**:
1. Import the file located at `postman/FastAPI-API-Postman-Collection.json` into Postman.
2. Update the base URL if necessary (e.g., `http://localhost:8000`).
3. Use the pre-configured requests to test the API endpoints.

## 📫 **Performance tests for the API**
Locust based tests can be used to load and stress test the API.
- [Performance Tests Documentation](performance_tests/README.md)

---
## 📚 **API Documentation**

FastAPI provides interactive API documentation for your project:

- **Swagger UI**: Interactive and easy-to-use API documentation.
  Access it at: [http://localhost:8000/docs](http://localhost:8000/docs)

- **ReDoc**: Comprehensive and clean API documentation.
  Access it at: [http://localhost:8000/redoc](http://localhost:8000/redoc)
