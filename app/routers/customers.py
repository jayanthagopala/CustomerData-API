from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..database import get_db
from ..utils.logger import setup_logger

router_logger = setup_logger("router-operations", "router.log")

router = APIRouter(
    prefix="/customers",
    tags=["Customers"],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "/", response_model=schemas.CustomerResponse, status_code=status.HTTP_201_CREATED
)
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    """
    Create a new customer.

    - **first_name**: The first name of the customer.
    - **last_name**: The last name of the customer.
    - **date_of_birth**: The date of birth of the customer (YYYY-MM-DD).
    """
    router_logger.debug(f"Creating customer: {customer}")
    return crud.create_customer(db=db, customer=customer)


@router.get("/", response_model=List[schemas.CustomerResponse])
def read_customers(
    skip: int = 0,
    limit: int = 10,
    start_date: str = None,
    end_date: str = None,
    db: Session = Depends(get_db),
):
    """
    Retrieve a paginated list of customers.

    - **skip**: Number of records to skip for pagination (default: 0).
    - **limit**: Maximum number of records to return (default: 10).
    - **start_date**: Start of the date range (YYYY-MM-DD).
    - **end_date**: End of the date range (YYYY-MM-DD).
    """
    if start_date and end_date:
        return crud.get_customers_by_date_range(
            db=db, start_date=start_date, end_date=end_date
        )
    else:
        # Existing pagination logic
        router_logger.debug(
            f"Retrieving customers with pagination: skip={skip}, limit={limit}"
        )
        if skip < 0 or limit < 1 or limit > 1000:
            router_logger.error(
                f"Invalid pagination parameters: skip={skip}, limit={limit}"
            )
            raise HTTPException(
                status_code=400,
                detail="Invalid pagination parameters. 'skip' must be >= 0 and 'limit' must be >= 1.",
            )

        customers = crud.get_customers(db=db, skip=skip, limit=limit)
        return customers


@router.get("/{customer_id}", response_model=schemas.CustomerResponse)
def read_customer(customer_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a customer's details by ID.

    - **customer_id**: The ID of the customer to retrieve.
    """
    router_logger.debug(f"Retrieving customer with ID {customer_id}")
    customer = crud.get_customer(db=db, customer_id=customer_id)
    if not customer:
        router_logger.error(f"Customer with ID {customer_id} not found")
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


@router.put("/{customer_id}", response_model=schemas.CustomerResponse)
def update_customer(
    customer_id: int, customer: schemas.CustomerUpdate, db: Session = Depends(get_db)
):
    """
    Update an existing customer.

    - **customer_id**: The ID of the customer to update.
    - **first_name**: Updated first name (optional).
    - **last_name**: Updated last name (optional).
    - **date_of_birth**: Updated date of birth (optional, YYYY-MM-DD).
    """
    router_logger.debug(f"Updating customer with ID {customer_id}: {customer}")
    updated_customer = crud.update_customer(
        db=db, customer_id=customer_id, customer=customer
    )
    if not updated_customer:
        router_logger.error(f"Customer with ID {customer_id} not found")
        raise HTTPException(status_code=404, detail="Customer not found")
    return updated_customer


@router.delete("/{customer_id}")
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    """
    Delete a customer by ID.

    - **customer_id**: The ID of the customer to delete.
    """
    router_logger.debug(f"Deleting customer with ID {customer_id}")
    success = crud.delete_customer(db=db, customer_id=customer_id)
    if not success:
        router_logger.error(f"Customer with ID {customer_id} not found")
        raise HTTPException(status_code=404, detail="Customer not found")
    return {"message": "Customer deleted successfully"}
