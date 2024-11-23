from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..database import get_db

router = APIRouter(
    prefix="/customers",
    tags=["Customers"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=schemas.CustomerResponse)
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    """
    Create a new customer.

    - **name**: The name of the customer
    - **email**: A valid email address
    - **age**: The age of the customer
    """
    print(f"Creating customer: {customer}")
    return crud.create_customer(db=db, customer=customer)


@router.get("/", response_model=List[schemas.CustomerResponse])
def read_customers(skip: int = 0, limit: int = 1000, db: Session = Depends(get_db)):
    """
    Retrieve a list of customers.

    - **skip**: Number of records to skip (default is 0)
    - **limit**: Maximum number of records to return (default is 10)
    """
    customers = crud.get_customers(db=db)
    return customers


@router.get("/{customer_id}", response_model=schemas.CustomerResponse)
def read_customer(customer_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a customer's details by ID.

    - **customer_id**: The ID of the customer to retrieve
    """
    customer = crud.get_customer(db=db, customer_id=customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


@router.put("/{customer_id}", response_model=schemas.CustomerResponse)
def update_customer(
    customer_id: int, customer: schemas.CustomerUpdate, db: Session = Depends(get_db)
):
    """
    Update an existing customer.

    - **customer_id**: The ID of the customer to update
    - **name**: Updated name (optional)
    - **email**: Updated email (optional)
    - **age**: Updated age (optional)
    """
    updated_customer = crud.update_customer(
        db=db, customer_id=customer_id, customer=customer
    )
    if not updated_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return updated_customer


@router.delete("/{customer_id}")
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    """
    Delete a customer by ID.

    - **customer_id**: The ID of the customer to delete
    """
    success = crud.delete_customer(db=db, customer_id=customer_id)
    if not success:
        raise HTTPException(status_code=404, detail="Customer not found")
    return {"message": "Customer deleted successfully"}
