from fastapi import APIRouter

from app.api.endpoints import (
    customers,
    services,
    appointments,
    past_appointments
)

api_router = APIRouter()

api_router.include_router(customers.router,
                          prefix='/customers',
                          tags=['customers'])
api_router.include_router(services.router,
                          prefix='/services',
                          tags=['services'])
api_router.include_router(appointments.router,
                          prefix='/appointments',
                          tags=['appointments'])
api_router.include_router(past_appointments.router,
                          prefix='/past_appointments',
                          tags=['past_appointments'])
