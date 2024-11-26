from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from typing import List

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

def get_customers_by_date_range(db: Session, start_date: str, end_date: str) -> List[Customer]:
    """
    Retrieve customers within a specific date of birth range.

    Args:
        db (Session): Database session
        start_date (str): Start date in YYYY-MM-DD format
        end_date (str): End date in YYYY-MM-DD format

    Returns:
        List[Customer]: List of customers within the specified date of birth range
    """
    try:
        crud_logger.debug(f"Retrieving customers with date of birth from {start_date} to {end_date}")
        
        # Validate date formats
        try:
            start_date_obj = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date_obj = datetime.strptime(end_date, "%Y-%m-%d").date()
            crud_logger.info(start_date_obj,end_date_obj)
        except ValueError:
            crud_logger.error("Invalid date format. Use YYYY-MM-DD.")
            raise HTTPException(
                status_code=400, detail="Invalid date format. Use YYYY-MM-DD."
            )

        # Ensure start date is before or equal to end date
        if start_date_obj > end_date_obj:
            crud_logger.error("Start date must be before or equal to end date.")
            raise HTTPException(
                status_code=400, detail="Start date must be before or equal to end date."
            )

        # Query customers by date of birth range
        customers = (
            db.query(Customer)
            .filter(Customer.date_of_birth >= start_date_obj, Customer.date_of_birth <= end_date_obj)
            .all()
        )
        return customers
    except SQLAlchemyError as e:
        crud_logger.exception(f"Error retrieving customers by date of birth range: {e}")
        raise HTTPException(status_code=500, detail="Internal server error.")
