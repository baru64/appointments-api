from typing import List, Any
from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api import deps
from app import schemas, crud

router = APIRouter()


@router.get("/", response_model=List[schemas.Appointment], status_code=200)
def read_past_appointments(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db)
) -> Any:
    past_appointments = crud.appointment.get_multiple(
        db, skip=skip, limit=limit, date_to=datetime.now()
    )
    return past_appointments
