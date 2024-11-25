# Performance Tests for FastAPI API

The tests simulate various user interactions to evaluate the API's performance under different scenarios, focusing on CRUD operations for the `/customers` endpoint.

---

## Test Scenarios

### 1. **Create Customer**
- **Description**: Simulates creating a new customer with valid data.
- **Frequency**: High (Weight: `3`)
- **Outcome**:
  - Successful customer creation.
  - Stores the `customer_id` for future operations.

### 2. **Get Customer**
- **Description**: Retrieves a single customer by `ID`.
- **Frequency**: Very High (Weight: `4`)
- **Outcome**:
  - Successfully fetches an existing customer.
  - Handles missing customers (`404`) by removing their IDs from the local list.

### 3. **Update Customer**
- **Description**: Updates an existing customer with new data.
- **Frequency**: Medium (Weight: `2`)
- **Outcome**:
  - Updates a customer if the `ID` exists.
  - Handles missing customers gracefully.

### 4. **Delete Customer**
- **Description**: Deletes a customer by `ID`.
- **Frequency**: Low (Weight: `1`)
- **Outcome**:
  - Successfully deletes the customer and removes the `ID` from the local list.

### 5. **Get All Customers**
- **Description**: Retrieves a paginated list of customers.
- **Frequency**: Low (Weight: `1`)
- **Outcome**:
  - Successfully retrieves customers with random pagination parameters.

### 6. **Create Invalid Customer**
- **Description**: Attempts to create a customer with invalid data (e.g., missing fields, invalid types).
- **Frequency**: Low (Weight: `1`)
- **Outcome**:
  - Expects validation errors (`422`).
  - Flags unexpected responses.

---

## User Classes

### **CustomerAPIUser**
- Simulates a general user interacting with the API.
- Tasks:
  - Create Customer
  - Get Customer
  - Update Customer
  - Delete Customer
  - Get All Customers
  - Create Invalid Customer

### **AdminUser**
- Extends `CustomerAPIUser` to simulate admin behavior.
- Task Weights:
  - **High**: Get all customers (Weight: `5`)
  - **Medium**: Create customers (Weight: `3`)

### **RegularUser**
- Extends `CustomerAPIUser` to simulate regular user behavior.
- Task Weights:
  - **High**: Get individual customers (Weight: `5`)
  - **Medium**: Update customers (Weight: `2`)

---

## Setup

### Prerequisites
Dev dependencies should be installed

### Install Dependencies
```bash

```
