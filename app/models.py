from sqlalchemy import Column, Date, Integer, String

from .database import Base


class Customer(Base):
    """
    The Customer model represents a customer in the application.
    It is mapped to the "customers" table in the database.
    """

    __tablename__ = "customers"

    # Define the columns of the "customers" table
    id = Column(Integer, primary_key=True, index=True)
    """
    The unique identifier for the customer, used as the primary key.
    Indexing the id column can improve query performance.
    """

    first_name = Column(String, index=True, nullable=False)
    """
    The customer's first name. Indexing this column can improve queries
    that filter or sort by first name. The field is required and cannot be null.
    """

    last_name = Column(String, index=True, nullable=False)
    """
    The customer's last name. Indexing this column can improve queries
    that filter or sort by last name. The field is required and cannot be null.
    """

    date_of_birth = Column(Date, index=True, nullable=False)
    """
    The customer's date of birth. Indexing this column can improve queries
    that filter or sort by date of birth. The field is required and cannot be null.
    """
