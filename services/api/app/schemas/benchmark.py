from pydantic import BaseModel, ConfigDict
from typing import List, Optional
import uuid
from datetime import datetime
from app.models.benchmark import RunStatus

class BenchmarkBase(BaseModel):
    name: str
    description: str
    version: str

class BenchmarkCreate(BenchmarkBase):
    pass

class BenchmarkResponse(BenchmarkBase):
    id: uuid.UUID
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class EvaluationRunResponse(BaseModel):
    id: uuid.UUID
    benchmark_id: uuid.UUID
    status: RunStatus
    total_cases: int
    completed_cases: int
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    model_config = ConfigDict(from_attributes=True)
