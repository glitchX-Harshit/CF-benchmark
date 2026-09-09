from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.scenario import scenario_repo
from app.models.scenario import Scenario

class ScenarioService:
    async def get_all(self, db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Scenario]:
        return await scenario_repo.get_multi(db, skip=skip, limit=limit)

scenario_service = ScenarioService()
