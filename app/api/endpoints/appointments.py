from typing import List, Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas, crud
from app.api import deps

router = APIRouter()


@router.post("/", response_model=schemas.Appointment, status_code=201)
def create_appointment(
    appointment: schemas.AppointmentCreate,
    db: Session = Depends(deps.get_db)
) -> Any:
    service = crud.service.get_by_id(db, appointment.service_id)
    if service is None:
        raise HTTPException(status_code=404, detail="Service not found")
    customer = crud.customer.get_by_id(db, appointment.customer_id)
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    # check available days and hours
    if appointment.date.weekday() not in service.available_days:
        raise HTTPException(status_code=409,
                            detail="Service not available at this date")
    if ((appointment.date + service.duration).time() > service.available_to
            or appointment.date.time < service.available_from):
        raise HTTPException(status_code=409,
                            detail="Service not available at this time")
    # check overlapping with other appointments
    other_appointments = crud.appointment.get_multiple(
        db,
        date_from=appointment.date - service.duration,
        date_to=appointment.date - service.duration
    )
    if (other_appointments is not None and
            len(other_appointments) >= service.customers_at_once):
        raise HTTPException(status_code=409,
                            detail="Service not available at this date")

    db_appointment = crud.appointment.create(db, appointment)
    return db_appointment


@router.get("/", response_model=List[schemas.Appointment], status_code=200)
def read_appointments(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db)
) -> Any:
    appointments = crud.appointment.get_multiple(db, skip=skip, limit=limit)
    return appointments


@router.get("/{appointment_id}",
            response_model=schemas.Appointment,
            status_code=200)
def read_appointment(
    appointment_id: int,
    db: Session = Depends(deps.get_db)
) -> Any:
    db_appointment = crud.appointment.get_by_id(db, appointment_id)
    if db_appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return db_appointment


@router.put("/{appointment_id}",
            response_model=schemas.Appointment,
            status_code=200)
def update_appointment(
    appointment_id: int,
    appointment: schemas.AppointmentUpdate,
    db: Session = Depends(deps.get_db)
) -> Any:
    db_appointment = crud.appointment.get_by_id(db, appointment_id)
    if db_appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    service = crud.service.get_by_id(db, appointment.service_id)
    if service is None:
        raise HTTPException(status_code=404, detail="Service not found")
    customer = crud.customer.get_by_id(db, appointment.customer_id)
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    # check available days and hours
    if appointment.date.weekday() not in service.available_days:
        raise HTTPException(status_code=409,
                            detail="Service not available at this date")
    if ((appointment.date + service.duration).time() > service.available_to
            or appointment.date.time < service.available_from):
        raise HTTPException(status_code=409,
                            detail="Service not available at this time")
    # check overlapping with other appointments
    other_appointments = crud.appointment.get_multiple(
        db,
        date_from=appointment.date - service.duration,
        date_to=appointment.date - service.duration,
        skip_id=appointment_id
    )
    if (other_appointments is not None and
            len(other_appointments) >= service.customers_at_once):
        raise HTTPException(status_code=409,
                            detail="Service not available at this date")

    db_appointment = crud.appointment.update(db, db_appointment, appointment)
    return db_appointment

# @router.patch("/{appointment_id}")
# def partial_update_appointment(appointment_id: int):
#     return {'test': 'asdf'}


@router.delete("/{appointment_id}",
               response_model=schemas.Appointment,
               status_code=200)
def delete_appointment(
    appointment_id: int,
    db: Session = Depends(deps.get_db)
) -> Any:
    db_appointment = crud.appointment.get_by_id(db, appointment_id)
    if db_appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    db_appointment = crud.appointment.remove(db, appointment_id)
    return db_appointment
