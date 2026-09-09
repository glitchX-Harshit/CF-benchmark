from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.db.session import async_session_maker

router = APIRouter()
public_router = APIRouter()

class HealthResponse(BaseModel):
    status: str

async def health_check() -> HealthResponse:
    return {"status": "ok"}

async def readiness_check() -> HealthResponse:
    try:
        async with async_session_maker() as session:
            await session.execute(text("SELECT 1"))
    except SQLAlchemyError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database is not ready.",
        ) from exc
    return {"status": "ready"}


router.get("", response_model=HealthResponse)(health_check)
router.get("/ready", response_model=HealthResponse)(readiness_check)
public_router.get("/health", response_model=HealthResponse)(health_check)
public_router.get("/ready", response_model=HealthResponse)(readiness_check)
