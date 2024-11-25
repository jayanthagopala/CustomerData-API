import random
from typing import Dict, Optional

from locust import HttpUser, between, task


class CustomerAPIUser(HttpUser):
    # Wait between 1 to 3 seconds between tasks
    wait_time = between(1, 3)

    def on_start(self):
        """Initialize user session data."""
        self.created_customer_ids = []
        self.test_customers = [
            {
                "first_name": f"TestFirstName{i}",
                "last_name": f"TestLastName{i}",
                "date_of_birth": f"19{random.randint(50, 99)}-01-{random.randint(10, 28)}",
            }
            for i in range(100)  # Pre-generate 100 test users
        ]

    @task(3)  # Higher weight for create operations
    def create_customer(self):
        """Create a new customer."""
        # Get a random test customer
        customer_data = random.choice(self.test_customers)

        with self.client.post(
            "/customers/", json=customer_data, catch_response=True
        ) as response:
            if response.status_code == 201:  # Resource created
                customer_id = response.json().get("id")
                if customer_id:
                    self.created_customer_ids.append(customer_id)
                response.success()
            else:
                response.failure(f"Failed to create customer: {response.text}")

    @task(4)  # Highest weight for read operations
    def get_customer(self):
        """Retrieve a customer by ID."""
        if not self.created_customer_ids:
            return

        customer_id = random.choice(self.created_customer_ids)
        with self.client.get(
            f"/customers/{customer_id}", catch_response=True
        ) as response:
            if response.status_code == 200:
                response.success()
            elif response.status_code == 404:
                # Remove ID if customer no longer exists
                self.created_customer_ids.remove(customer_id)
                response.success()
            else:
                response.failure(f"Failed to get customer: {response.text}")

    @task(2)  # Medium weight for update operations
    def update_customer(self):
        """Update an existing customer."""
        if not self.created_customer_ids:
            return

        customer_id = random.choice(self.created_customer_ids)
        update_data = {
            "first_name": f"UpdatedFirstName{random.randint(1, 1000)}",
            "last_name": f"UpdatedLastName{random.randint(1, 1000)}",
        }

        with self.client.put(
            f"/customers/{customer_id}", json=update_data, catch_response=True
        ) as response:
            if response.status_code == 200:
                response.success()
            elif response.status_code == 404:
                self.created_customer_ids.remove(customer_id)
                response.success()
            else:
                response.failure(f"Failed to update customer: {response.text}")

    @task(1)  # Lowest weight for delete operations
    def delete_customer(self):
        """Delete a customer."""
        if not self.created_customer_ids:
            return

        customer_id = random.choice(self.created_customer_ids)
        with self.client.delete(
            f"/customers/{customer_id}", catch_response=True
        ) as response:
            if response.status_code in [200, 204]:
                self.created_customer_ids.remove(customer_id)
                response.success()
            elif response.status_code == 404:
                self.created_customer_ids.remove(customer_id)
                response.success()
            else:
                response.failure(f"Failed to delete customer: {response.text}")

    @task(1)
    def get_all_customers(self):
        """Retrieve all customers with pagination."""
        params = {"skip": random.randint(0, 50), "limit": random.randint(10, 50)}

        with self.client.get(
            "/customers/", params=params, catch_response=True
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Failed to get customers list: {response.text}")

    @task(1)
    def create_invalid_customer(self):
        """Attempt to create a customer with invalid data."""
        invalid_data = {
            "first_name": "InvalidFirstName",
            # Missing required last_name and date_of_birth fields
        }

        with self.client.post(
            "/customers/", json=invalid_data, catch_response=True
        ) as response:
            if response.status_code == 422:  # Expected validation error
                response.success()
            else:
                response.failure(
                    f"Unexpected response for invalid data: {response.text}"
                )


class AdminUser(CustomerAPIUser):
    """Simulates admin user behavior with different weights."""

    @task(5)
    def get_all_customers(self):
        """Admins frequently list all customers."""
        super().get_all_customers()

    @task(3)
    def create_customer(self):
        """Admins create customers less frequently."""
        super().create_customer()


class RegularUser(CustomerAPIUser):
    """Simulates regular user behavior with different weights."""

    @task(5)
    def get_customer(self):
        """Regular users mostly read individual records."""
        super().get_customer()

    @task(2)
    def update_customer(self):
        """Regular users update records occasionally."""
        super().update_customer()
