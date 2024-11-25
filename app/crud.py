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


def get_customer_by_email(db: Session, email: str):
    """
    Retrieve a customer by their email.
    """
    crud_logger.debug(f"Retrieving customer with email {email}")
    return db.query(Customer).filter(Customer.email == email).first()


def create_customer(db: Session, customer: CustomerCreate):
    """
    Create a new customer.
    If a customer with the same email already exists, raises an exception.
    """
    crud_logger.debug(f"Creating customer with email {customer.email}")
    existing_customer = get_customer_by_email(db, customer.email)
    if existing_customer:
        raise HTTPException(
            status_code=400, detail="A customer with this email already exists."
        )
    new_customer = Customer(
        **customer.model_dump()  # Use model_dump() to handle Pydantic models properly
    )
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return new_customer


def get_customers(db: Session):
    """
    Retrieve all customers.
    """
    crud_logger.debug("Retrieving all customers")
    return db.query(Customer).all()


def update_customer(db: Session, customer_id: int, customer: CustomerUpdate):
    crud_logger.debug(f"Updating customer with ID {customer_id}")
    db_customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not db_customer:
        raise HTTPException(
            status_code=404, detail=f"Customer with ID {customer_id} not found."
        )

    customer_data = customer.model_dump(exclude_unset=True)

    if not customer_data:  # Reject empty updates
        crud_logger.error("No fields provided for update.")
        raise HTTPException(
            status_code=400, detail="At least one field must be provided for update."
        )
    # Check for duplicate email
    if "email" in customer_data:
        existing_customer = (
            db.query(Customer)
            .filter(
                Customer.email == customer_data["email"], Customer.id != customer_id
            )
            .first()
        )
        if existing_customer:
            crud_logger.error(
                f"Customer with email {customer_data['email']} already exists."
            )
            raise HTTPException(
                status_code=400,
                detail="A customer with this email already exists.",
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
    db_customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not db_customer:
        crud_logger.error(f"Customer with ID {customer_id} not found.")
        raise HTTPException(
            status_code=404, detail=f"Customer with ID {customer_id} not found."
        )

    db.delete(db_customer)
    db.commit()
    return True
