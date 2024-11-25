from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr


class CustomerBase(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: date


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: Optional[date] = None


class CustomerResponse(CustomerBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
