from fastapi import APIRouter

router = APIRouter()


@router.post("/")
def create_customer():
    return {'test': 'asdf'}


@router.get("/")
def read_customers():
    return {'test': 'asdf'}


@router.get("/{customer_id}")
def read_customer(customer_id: int):
    return {'test': 'asdf'}


@router.put("/{customer_id}")
def update_customer(customer_id: int):
    return {'test': 'asdf'}


# @router.patch("/{customer_id}")
# def partial_update_customer(customer_id: int):
#     return {'test': 'asdf'}


@router.delete("/{customer_id}")
def delete_customer(customer_id: int):
    return {'test': 'asdf'}
