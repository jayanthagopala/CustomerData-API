from sqlalchemy.orm import Session

from .models import Customer
from .schemas import CustomerCreate, CustomerUpdate


def create_customer(db: Session, customer: CustomerCreate):
    new_customer = Customer(**customer.dict())
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return new_customer


def get_customer(db: Session, customer_id: int):
    return db.query(Customer).filter(Customer.id == customer_id).first()


def update_customer(db: Session, customer_id: int, customer: CustomerUpdate):
    db_customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if db_customer:
        for key, value in customer.dict(exclude_unset=True).items():
            setattr(db_customer, key, value)
        db.commit()
        db.refresh(db_customer)
        return db_customer
    return None


def delete_customer(db: Session, customer_id: int):
    db_customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if db_customer:
        db.delete(db_customer)
        db.commit()
        return True
    return False
