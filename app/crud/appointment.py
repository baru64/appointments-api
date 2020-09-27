from typing import List, Optional
from datetime import datetime

from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app import models, schemas


def get_by_id(
    db: Session,
    appointment_id: int
) -> Optional[models.Appointment]:
    return db.query(models.Appointment) \
             .filter(models.Appointment.id == appointment_id).first()


def get_multiple(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None,
    skip_id: int = None
) -> List[models.Appointment]:
    q = db.query(models.Appointment).offset(skip).limit(limit)
    if date_from is not None:
        q = q.filter(models.Appointment.date >= date_from)
    if date_to is not None:
        q = q.filter(models.Appointment.date <= date_to)
    if skip_id is not None:
        q = q.filter(models.Appointment.id != skip_id)
    return q.all()


def create(
    db: Session,
    appointment: schemas.AppointmentCreate
) -> models.Appointment:
    db_appointment = models.Appointment(
        description=appointment.description,
        date=appointment.date,
        service_id=appointment.service_id,
        customer_id=appointment.customer_id
    )
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment


def update(
    db: Session,
    db_appointment: models.Appointment,
    appointment_in: schemas.AppointmentUpdate
) -> models.Appointment:
    appointment_data = jsonable_encoder(db_appointment)
    if isinstance(appointment_data, dict):
        update_data = appointment_data
    else:
        update_data = db_appointment.dict(exclude_unset=True)
    for field in db_appointment:
        if field in update_data:
            setattr(db_appointment, field, update_data[field])
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment


def remove(db: Session, appointment_id: int) -> models.Appointment:
    db_appointment = db.query(models.Appointment).get(id)
    db.delete(db_appointment)
    db.commit()
    return db_appointment
