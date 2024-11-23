from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import Customer
from app.schemas import CustomerCreate, CustomerUpdate


def get_customer(db: Session, customer_id: int):
    """
    Retrieve a customer by their ID.
    """
    return db.query(Customer).filter(Customer.id == customer_id).first()


def get_customer_by_email(db: Session, email: str):
    """
    Retrieve a customer by their email.
    """
    return db.query(Customer).filter(Customer.email == email).first()


def create_customer(db: Session, customer: CustomerCreate):
    """
    Create a new customer.
    If a customer with the same email already exists, raises an exception.
    """
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
    return db.query(Customer).all()


def update_customer(db: Session, customer_id: int, customer: CustomerUpdate):
    """
    Update an existing customer.
    Only updates fields provided in the CustomerUpdate schema.
    """
    db_customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found.")

    # Update only provided fields
    customer_data = customer.model_dump(exclude_unset=True)
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
        raise HTTPException(status_code=404, detail="Customer not found.")

    db.delete(db_customer)
    db.commit()
    return True
