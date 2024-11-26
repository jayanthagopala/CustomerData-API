# Customer API Load Testing

## Overview

This Locust-based load testing framework simulates various user interactions with a Customer API, including create, read, update, and delete (CRUD) operations. The test suite is designed to mimic different user behaviors and test the performance and reliability of the API under various scenarios.

## Prerequisites

- Python 3.8+
- Poetry (for dependency management)

## Installation

1. Clone the repository
2. Install dependencies using Poetry:
   ```bash
   poetry install
   ```

## Running the Tests

```bash
locust -f performance_tests/locustfile.py
```

This will start the Locust web interface where you can configure:
- Number of users
- Spawn rate
- Host URL

## Test Scenarios

### User Types

1. **CustomerAPIUser (Base Class)**
   - Performs balanced CRUD operations
   - Weights:
     - Create: 3
     - Read: 4
     - Update: 2
     - Delete: 1
     - List All: 1

2. **AdminUser**
   - Focuses on listing and creating customers
   - Higher frequency of listing all customers

3. **RegularUser**
   - Focuses on reading and occasional updates
   - Primarily retrieves individual customer records

### Key Operations

- Create Customer
- Get Customer by ID
- Update Customer
- Delete Customer
- List Customers (with pagination)
- Validate API error handling

## Test Data Generation

- Randomly generates customer data
- Creates 100 pre-generated test customers
- Handles dynamic customer ID tracking

## Error Handling

- Tracks created customer IDs
- Removes IDs for non-existent customers
- Validates response status codes
- Simulates invalid data creation

## Best Practices

- Random wait time between 1-3 seconds between tasks
- Realistic operation weights
- Dynamic data generation
- Error tracking and removal of stale IDs

## Customization

Modify the script to:
- Adjust task weights
- Change test data generation
- Add more complex scenarios
