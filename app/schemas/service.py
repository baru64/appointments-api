from typing import Optional
from datetime import time

from pydantic import BaseModel


class ServiceBase(BaseModel):
    name: str
    description: Optional[str]
    customers_at_once: int = 1
    available_from: time
    available_to: time
    available_days: str = "0,1,2,3,4"
    duration: time
    price: int


class ServiceCreate(ServiceBase):
    pass


class ServiceUpdate(ServiceBase):
    pass


class ServiceInDBBase(ServiceBase):
    id: Optional[int]

    class Config:
        orm_mode = True


class Service(ServiceInDBBase):
    pass


class ServiceInDB(ServiceInDBBase):
    pass
