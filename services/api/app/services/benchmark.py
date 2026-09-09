from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.benchmark import benchmark_repo
from app.models.benchmark import Benchmark

class BenchmarkService:
    async def get_all(self, db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Benchmark]:
        return await benchmark_repo.get_multi(db, skip=skip, limit=limit)

benchmark_service = BenchmarkService()
