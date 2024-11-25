from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import Customer
from app.schemas import CustomerCreate, CustomerUpdate
from app.utils.logger import setup_logger

crud_logger = setup_logger("crud-operations", "crud.log")


def get_customer(db: Session, customer_id: int):
    """
    Retrieve a customer by their ID.
    """
    crud_logger.debug(f"Retrieving customer with ID {customer_id}")
    return db.query(Customer).filter(Customer.id == customer_id).first()


def create_customer(db: Session, customer: CustomerCreate):
    """
    Create a new customer.
    """
    crud_logger.debug(
        f"Creating customer: first_name={customer.first_name}, last_name={customer.last_name}"
    )
    new_customer = Customer(
        first_name=customer.first_name,
        last_name=customer.last_name,
        date_of_birth=customer.date_of_birth,
    )
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return new_customer


def get_customers(db: Session, skip: int = 0, limit: int = 10):
    """
    Retrieve a paginated list of customers.
    """
    crud_logger.debug(f"Retrieving customers with skip={skip}, limit={limit}")
    return db.query(Customer).offset(skip).limit(limit).all()


def update_customer(db: Session, customer_id: int, customer: CustomerUpdate):
    """
    Update an existing customer.
    """
    crud_logger.debug(f"Updating customer with ID {customer_id}")
    db_customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not db_customer:
        crud_logger.error(f"Customer with ID {customer_id} not found.")
        raise HTTPException(
            status_code=404, detail=f"Customer with ID {customer_id} not found."
        )

    customer_data = customer.model_dump(exclude_unset=True)

    if not customer_data:  # Reject empty updates
        crud_logger.error("No fields provided for update.")
        raise HTTPException(
            status_code=400, detail="At least one field must be provided for update."
        )

    for key, value in customer_data.items():
        setattr(db_customer, key, value)

    db.commit()
    db.refresh(db_customer)
    return db_customer


def delete_customer(db: Session, customer_id: int):
    """
    Delete a customer by ID.
    """
    crud_logger.debug(f"Deleting customer with ID {customer_id}")
    db_customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not db_customer:
        crud_logger.error(f"Customer with ID {customer_id} not found.")
        raise HTTPException(
            status_code=404, detail=f"Customer with ID {customer_id} not found."
        )

    db.delete(db_customer)
    db.commit()
    return True
