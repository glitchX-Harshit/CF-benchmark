from fastapi import APIRouter

api_router = APIRouter()

from .health import router as health_router
from .scenarios import router as scenarios_router
from .evaluations import router as evaluations_router
from .benchmarks import router as benchmarks_router
from .analytics import router as analytics_router

api_router.include_router(health_router, prefix="/health", tags=["health"])
api_router.include_router(scenarios_router, prefix="/scenarios", tags=["scenarios"])
api_router.include_router(evaluations_router, prefix="/evaluations", tags=["evaluations"])
api_router.include_router(benchmarks_router, prefix="/benchmarks", tags=["benchmarks"])
api_router.include_router(analytics_router, prefix="/analytics", tags=["analytics"])
