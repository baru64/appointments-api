from pydantic import BaseSettings


class Settings(BaseSettings):
    API_STR: str = '/api'
    PROJECT_NAME: str = 'Appointments'
    SQLALCHEMY_DATABASE_URL = "sqlite:///app.db"


settings = Settings()
