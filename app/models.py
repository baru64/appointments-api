from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    Time,
    DateTime,
    Interval
)
from sqlalchemy.orm import relationship

from app.database import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    tel_number = Column(String)
    email = Column(String)

    appointments = relationship("Appointment", cascade="all, delete",
                                back_populates="customer")


class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)
    customers_at_once = Column(Integer)
    available_from = Column(Time)
    available_to = Column(Time)
    available_days = Column(String)
    duration = Column(Interval)
    price = Column(Integer)

    appointments = relationship("Appointment", cascade="all, delete",
                                back_populates="service")


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    date = Column(DateTime)
    service_id = Column(Integer, ForeignKey("services.id"))
    customer_id = Column(Integer, ForeignKey("customers.id"))

    service = relationship("Service", back_populates="appointments")
    customer = relationship("Customer", back_populates="appointments")
