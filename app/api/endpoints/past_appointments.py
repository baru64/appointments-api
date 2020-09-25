from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def read_past_appointments():
    return {'test': 'asdf'}
