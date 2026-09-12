from fastapi import APIRouter
from .v1 import health, evaluations, benchmarks, evaluate

api_router = APIRouter()
api_router.include_router(health.router, prefix="/v1", tags=["health"])
api_router.include_router(evaluations.router, prefix="/v1/evaluations", tags=["evaluations"])
api_router.include_router(benchmarks.router, prefix="/v1/benchmarks", tags=["benchmarks"])
api_router.include_router(evaluate.router, prefix="/v1/evaluate", tags=["evaluate"])
