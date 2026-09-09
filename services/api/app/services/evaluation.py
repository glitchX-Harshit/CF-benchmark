from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.evaluation import evaluation_repo
from app.models.evaluation import Evaluation

class EvaluationService:
    async def get_all(self, db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Evaluation]:
        return await evaluation_repo.get_multi(db, skip=skip, limit=limit)

evaluation_service = EvaluationService()
