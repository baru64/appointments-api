from sqlalchemy import Column, ForeignKey, Integer, String, Time, DateTime
from sqlalchemy.orm import relationship

from app.database import Base


class Consumer(Base):
    __tablename__ = "consumers"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    tel_number = Column(String)
    email = Column(String)

    appointments = relationship("Appointments", back_populates="consumer")


class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)
    consumers_at_once = Column(Integer)
    availible_from = Column(Time)
    availible_to = Column(Time)
    availible_days = Column(String)
    duration = Column(Time)
    price = Column(Integer)

    appointments = relationship("Appointments", back_populates="service")


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    date = Column(DateTime)
    service_id = Column(Integer, ForeignKey("services.id"))
    consumer_id = Column(Integer, ForeignKey("consumers.id"))

    service = relationship("Service", back_populates="appointments")
    consumer = relationship("Consumer", back_populates="appointments")
