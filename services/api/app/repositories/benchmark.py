from app.repositories.base import BaseRepository
from app.models.benchmark import Benchmark

class BenchmarkRepository(BaseRepository[Benchmark]):
    pass

benchmark_repo = BenchmarkRepository(Benchmark)
