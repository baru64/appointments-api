from zlib import adler32

from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    Time,
    DateTime,
    Interval,
    Boolean
)
from sqlalchemy.orm import relationship

from app.database import Base


# class User(Base):
#     __tablename__ = "users"
#
#     id = Column(Integer, primary_key=True, index=True)
#     email = Column(String, unique=True, index=True, nullable=False)
#     hashed_password = Column(String, nullable=False)
#     is_superuser = Column(Boolean(), default=False)
#
#     customer = relationship("Customer", cascade="all, delete",
#                             back_populates="user")


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    tel_number = Column(String)
    email = Column(String)

#     user = relationship("User", single_parent=True,
#                         back_populates="customer")
    appointments = relationship("Appointment", cascade="all, delete",
                                back_populates="customer")

    def get_checksum(self) -> int:
        data_str = "{}{}{}{}".format(self.first_name, self.last_name,
                                     self.tel_number, self.email)
        data_b = data_str.encode('utf-8')
        return adler32(data_b)


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

    def get_checksum(self) -> int:
        data_str = "{}{}{}{}{}{}{}{}".format(
            self.name, self.description, self.customers_at_once,
            self.available_from, self.available_to,
            self.available_days, self.duration, self.price)
        data_b = data_str.encode('utf-8')
        return adler32(data_b)


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    date = Column(DateTime)
    service_id = Column(Integer, ForeignKey("services.id"))
    customer_id = Column(Integer, ForeignKey("customers.id"))

    service = relationship("Service", back_populates="appointments")
    customer = relationship("Customer", back_populates="appointments")

    def get_checksum(self) -> int:
        data_str = "{}{}{}{}".format(self.description,self.date,
                                     self.service_id,self.customer_id)
        data_b = data_str.encode('utf-8')
        return adler32(data_b)
