# FastAPI-Based Customer Data Management System

A Python-based project built with FastAPI, designed to deliver efficient and scalable APIs with a simple yet extensible structure.

- Provides endpoints for creating, retrieving, updating, and deleting customer records.
- Supports advanced features such as filtering, pagination, and sorting to ensure efficient and flexible data retrieval.

---

## 🛠️ **Endpoints Overview**

### **1. Root**
`GET /`
Returns a welcome message.

### **2. Customers**
| Method | Endpoint                | Description                               |
|--------|--------------------------|-------------------------------------------|
| POST   | `/customers/`           | Create a new customer                     |
| GET    | `/customers/`           | List customers with pagination support    |
| GET    | `/customers/{id}`       | Retrieve a customer by ID                 |
| DELETE | `/customers/{id}`       | Delete a customer by ID                   |

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

- **In-Memory Data Storage (Prototyping)**:
  - Supports rapid prototyping with an in-memory SQLite database for quick iteration.
  - Configurable to use production-ready databases like PostgreSQL or MySQL.

- **Scalable and Extensible Design**:
  - Modular architecture with separate files for routing, database models, and schemas.
  - Easily extendable to include more features or new endpoints.

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
│   ├── __init__.py        # Marks the app directory as a Python module
│   ├── main.py            # Main FastAPI application and routes
│   ├── schemas.py         # Pydantic schemas for request/response validation
├── tests/
│   ├── __init__.py        # Marks the tests directory as a Python module
│   ├── test_main.py       # Test cases for API endpoints
├── .env                   # Environment variables (e.g., DB connections)
├── .pre-commit-config.yaml # Pre-commit hooks for code quality checks
├── pyproject.toml         # Poetry configuration and dependencies
└── README.md              # Project documentation
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

---
## 📚 **API Documentation**

FastAPI provides interactive API documentation for your project:

- **Swagger UI**: Interactive and easy-to-use API documentation.
  Access it at: [http://localhost:8000/docs](http://localhost:8000/docs)

- **ReDoc**: Comprehensive and clean API documentation.
  Access it at: [http://localhost:8000/redoc](http://localhost:8000/redoc)
