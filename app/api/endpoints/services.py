from typing import List, Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas, crud
from app.api import deps

router = APIRouter()


@router.post("/", response_model=schemas.Service, status_code=201)
def create_service(
    service: schemas.ServiceCreate,
    db: Session = Depends(deps.get_db)
) -> Any:
    db_service = crud.service.create(db, service)
    return db_service


@router.get("/", response_model=List[schemas.Service], status_code=200)
def read_services(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db)
) -> Any:
    services = crud.service.get_multiple(db, skip=skip, limit=limit)
    return services


@router.get("/{service_id}", response_model=schemas.Service, status_code=200)
def read_service(
    service_id: int,
    db: Session = Depends(deps.get_db)
) -> Any:
    db_service = crud.service.get_by_id(db, service_id)
    if db_service is None:
        raise HTTPException(status_code=404, detail="Service not found")
    return db_service


@router.put("/{service_id}", response_model=schemas.Service, status_code=200)
def update_service(
    service_id: int,
    service: schemas.ServiceUpdate,
    db: Session = Depends(deps.get_db)
) -> Any:
    db_service = crud.service.get_by_id(db, service_id)
    if db_service is None:
        raise HTTPException(status_code=404, detail="Service not found")
    db_service = crud.service.update(db, db_service, service)
    return db_service

# @router.patch("/{service_id}")
# def partial_update_service(service_id: int):
#     return {'test': 'asdf'}


@router.delete("/{service_id}",
               response_model=schemas.Service,
               status_code=200)
def delete_service(
    service_id: int,
    db: Session = Depends(deps.get_db)
) -> Any:
    db_service = crud.service.get_by_id(db, service_id)
    if db_service is None:
        raise HTTPException(status_code=404, detail="Service not found")
    db_service = crud.service.remove(db, service_id)
    return db_service
