from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import uuid

from app.api.deps import get_db
from app.schemas.benchmark import BenchmarkCreate, BenchmarkResponse
from app.schemas.common import PaginatedResponse
from app.services.benchmark import benchmark_service

router = APIRouter()

@router.get("", response_model=PaginatedResponse[BenchmarkResponse])
async def list_benchmarks(page: int = 1, size: int = 50, db: AsyncSession = Depends(get_db)):
    offset = (page - 1) * size
    benchmarks = await benchmark_service.get_all(db, skip=offset, limit=size)
    return PaginatedResponse(items=list(benchmarks), total=len(benchmarks), page=page, size=size)
