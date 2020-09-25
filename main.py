from fastapi import FastAPI

from app.config import settings
from app.api.api import api_router
from app.database import engine
from app import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_STR}/openapi.json"
)

app.include_router(api_router, prefix=settings.API_STR)
