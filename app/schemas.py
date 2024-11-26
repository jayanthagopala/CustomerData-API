from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict


# Base class for a customer, defining the common fields
class CustomerBase(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: date


# Create a new customer, inheriting from CustomerBase
class CustomerCreate(CustomerBase):
    pass


# Update an existing customer, allowing optional fields
class CustomerUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: Optional[date] = None


# Response model for a customer, inheriting from CustomerBase and adding an ID field
class CustomerResponse(CustomerBase):
    id: int

    # Configure the Pydantic model to use attributes instead of dictionary keys
    model_config = ConfigDict(from_attributes=True)
