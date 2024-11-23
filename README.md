
# FastAPI-API

A Python-based FastAPI project designed for building efficient and scalable APIs with a simple yet extensible structure.

---

## 🚀 **Features**
- FastAPI framework for building APIs.
- Automatic data validation using Pydantic.
- In-memory data storage for prototyping.
- Designed with scalability in mind.
- Pre-commit hooks for automated code formatting and quality checks.

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

## 🛠️ **Endpoints Overview**

### **1. Root**
`GET /`
Returns a welcome message.

### **2. Customers**
| Method | Endpoint                | Description                 |
|--------|--------------------------|-----------------------------|
| POST   | `/customers/`           | Create a new customer       |
| GET    | `/customers/`           | List all customers          |
| GET    | `/customers/{id}`       | Retrieve a customer by ID   |
| DELETE | `/customers/{id}`       | Delete a customer by ID     |

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

## Postman Collection
A Postman collection is provided to test the API.

**Steps to Use**:
1. Import the file located at `postman/FastAPI-API-Postman-Collection.json` into Postman.
2. Update the base URL if necessary (e.g., `http://localhost:8000`).
3. Use the pre-configured requests to test the API endpoints.
