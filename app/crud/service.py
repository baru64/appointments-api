from typing import List, Optional

from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app import models, schemas


def get_by_id(db: Session, service_id: int) -> Optional[models.Service]:
    return db.query(models.Service) \
             .filter(models.Service.id == service_id).first()


def get_multiple(
    db: Session,
    skip: int = 0,
    limit: int = 100
) -> List[models.Service]:
    return db.query(models.Service).offset(skip).limit(limit).all()


def create(db: Session, service: schemas.ServiceCreate) -> models.Service:
    db_service = models.Service(
        name=service.name,
        description=service.description,
        customers_at_once=service.customers_at_once,
        available_from=service.available_from,
        available_to=service.available_to,
        available_days=service.available_days,
        duration=service.duration,
        price=service.price
    )
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    return db_service


def update(
    db: Session,
    db_service: models.Service,
    service_in: schemas.ServiceUpdate
) -> models.Customer:
    service_data = jsonable_encoder(db_service)
    if isinstance(service_data, dict):
        update_data = service_data
    else:
        update_data = db_service.dict(exclude_unset=True)
    for field in db_service:
        if field in update_data:
            setattr(db_service, field, update_data[field])
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    return db_service


def remove(db: Session, service_id: int) -> models.Service:
    db_service = db.query(models.Service).get(id)
    db.delete(db_service)
    db.commit()
    return db_service
