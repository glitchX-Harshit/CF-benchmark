from app.repositories.base import BaseRepository
from app.models.evaluation import Evaluation

class EvaluationRepository(BaseRepository[Evaluation]):
    pass

evaluation_repo = EvaluationRepository(Evaluation)
