from typing import List, Optional

from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app import models, schemas


def get_by_id(db: Session, customer_id: int) -> Optional[models.Customer]:
    return db.query(models.Customer) \
             .filter(models.Customer.id == customer_id).first()


def get_multiple(
    db: Session,
    skip: int = 0,
    limit: int = 100
) -> List[models.Customer]:
    return db.query(models.Customer).offset(skip).limit(limit).all()


def create(db: Session, customer: schemas.CustomerCreate) -> models.Customer:
    db_customer = models.Customer(
        first_name=customer.first_name,
        last_name=customer.last_name,
        tel_number=customer.tel_number,
        email=customer.email
    )
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer


def update(
    db: Session,
    db_customer: models.Customer,
    customer_in: schemas.CustomerUpdate
) -> models.Customer:
    customer_data = jsonable_encoder(db_customer)
    if isinstance(customer_data, dict):
        update_data = customer_data
    else:
        update_data = db_customer.dict(exclude_unset=True)
    for field in db_customer:
        if field in update_data:
            setattr(db_customer, field, update_data[field])
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer


def remove(db: Session, customer_id: int) -> models.Customer:
    db_customer = db.query(models.Customer).get(id)
    db.delete(db_customer)
    db.commit()
    return db_customer
