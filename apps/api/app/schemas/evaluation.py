from pydantic import BaseModel
from typing import Dict, Any

class EvaluationRequest(BaseModel):
    scenario_id: str
    response: str

class EvaluationResponse(BaseModel):
    id: str
    scenario_id: str
    result: Dict[str, Any]
    overall_score: float
