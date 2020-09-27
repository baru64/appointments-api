from typing import Optional

from pydantic import BaseModel


class CustomerBase(BaseModel):
    first_name: str
    last_name: Optional[str] = None
    tel_number: Optional[str] = None
    email: Optional[str] = None


# Properties to receive on creation
class CustomerCreate(CustomerBase):
    pass


# Properties to receive on update
class CustomerUpdate(CustomerBase):
    pass


class CustomerInDBBase(CustomerBase):
    id: int

    class Config:
        orm_mode = True


# Properties received from API
class Customer(CustomerInDBBase):
    pass


# Properties stored in database
class CustomerInDB(CustomerInDBBase):
    pass
