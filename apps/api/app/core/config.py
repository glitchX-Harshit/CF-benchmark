import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "ClozFlow"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://clozflow:clozflow_password@localhost:5432/clozflow")
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    class Config:
        env_file = ".env"

settings = Settings()
