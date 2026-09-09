from app.repositories.base import BaseRepository
from app.models.scenario import Scenario

class ScenarioRepository(BaseRepository[Scenario]):
    pass

scenario_repo = ScenarioRepository(Scenario)
