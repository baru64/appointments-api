from typing import List, Any, Optional

from fastapi import APIRouter, Depends, HTTPException, Response, Header
from sqlalchemy.orm import Session

from app import schemas, crud
from app.api import deps

router = APIRouter()


@router.post("/", response_model=schemas.Customer, status_code=201)
def create_customer(
    response: Response,
    customer: schemas.CustomerCreate,
    db: Session = Depends(deps.get_db)
) -> Any:
    db_customer = crud.customer.create(db, customer)
    response.headers['ETag'] = str(db_customer.get_checksum())
    return db_customer


@router.get("/", response_model=List[schemas.Customer], status_code=200)
def read_customers(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db)
) -> Any:
    customers = crud.customer.get_multiple(db, skip=skip, limit=limit)
    return customers


@router.get("/{customer_id}", response_model=schemas.Customer, status_code=200)
def read_customer(
    response: Response,
    customer_id: int,
    db: Session = Depends(deps.get_db)
) -> Any:
    db_customer = crud.customer.get_by_id(db, customer_id)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    response.headers['ETag'] = str(db_customer.get_checksum())
    return db_customer


@router.put("/{customer_id}", response_model=schemas.Customer, status_code=200)
def update_customer(
    response: Response,
    customer_id: int,
    customer: schemas.CustomerUpdate,
    db: Session = Depends(deps.get_db),
    if_match: Optional[str] = Header(None)
) -> Any:
    db_customer = crud.customer.get_by_id(db, customer_id)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    etag = db_customer.get_checksum()
    if str(etag) != if_match:
        raise HTTPException(status_code=412,
                            detail="ETag doesn't match current resource state")
    db_customer = crud.customer.update(db, db_customer, customer)
    response.headers['ETag'] = str(db_customer.get_checksum())
    return db_customer

# @router.patch("/{customer_id}")
# def partial_update_customer(customer_id: int):
#     return {'test': 'asdf'}


@router.delete("/{customer_id}",
               response_model=schemas.Customer,
               status_code=200)
def delete_customer(
    customer_id: int,
    db: Session = Depends(deps.get_db)
) -> Any:
    db_customer = crud.customer.get_by_id(db, customer_id)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    db_customer = crud.customer.remove(db, customer_id)
    return db_customer
