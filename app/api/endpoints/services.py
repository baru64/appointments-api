from fastapi import APIRouter

router = APIRouter()


@router.post("/")
def create_service():
    return {'test': 'asdf'}


@router.get("/")
def read_services():
    return {'test': 'asdf'}


@router.get("/{service_id}")
def read_service(service_id: int):
    return {'test': 'asdf'}


@router.put("/{service_id}")
def update_service(service_id: int):
    return {'test': 'asdf'}


# @router.patch("/{customer_id}")
# def partial_update_customer(customer_id: int):
#     return {'test': 'asdf'}


@router.delete("/{service_id}")
def delete_service(service_id: int):
    return {'test': 'asdf'}
