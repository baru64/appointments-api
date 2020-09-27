from typing import Optional
from datetime import datetime

from pydantic import BaseModel


class AppointmentBase(BaseModel):
    description: Optional[str]
    date: datetime


# Properties to receive on creation
class AppointmentCreate(AppointmentBase):
    service_id: int
    customer_id: Optional[int]


class AppointmentUpdate(AppointmentBase):
    service_id: int
    customer_id: int


class AppointmentInDBBase(AppointmentBase):
    id: int
    service_id: int
    customer_id: int

    class Config:
        orm_mode = True


# Properties received from API
class Appointment(AppointmentInDBBase):
    pass


# Properties stored in database
class AppointmentInDB(AppointmentInDBBase):
    pass
