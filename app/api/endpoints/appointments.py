from fastapi import APIRouter

router = APIRouter()


@router.post("/")
def create_appointment():
    return {'test': 'asdf'}


@router.get("/")
def read_appointments():
    return {'test': 'asdf'}


@router.get("/{appointment_id}")
def read_appointment(appointment_id: int):
    return {'test': 'asdf'}


@router.put("/{appointment_id}")
def update_appointment(appointment_id: int):
    return {'test': 'asdf'}


# @router.patch("/{appointment_id}")
# def partial_update_customer(appointment_id: int):
#     return {'test': 'asdf'}


@router.delete("/{appointment_id}")
def delete_appointment(appointment_id: int):
    return {'test': 'asdf'}
