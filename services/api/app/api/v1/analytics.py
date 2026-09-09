from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.schemas.analytics import AnalyticsOverview, AnalyticsDimensions
from app.services.analytics import analytics_service

router = APIRouter()

@router.get("/overview", response_model=AnalyticsOverview)
async def get_overview(db: AsyncSession = Depends(get_db)):
    return await analytics_service.get_overview(db)

@router.get("/dimensions", response_model=AnalyticsDimensions)
async def get_dimensions(db: AsyncSession = Depends(get_db)):
    return await analytics_service.get_dimensions(db)
