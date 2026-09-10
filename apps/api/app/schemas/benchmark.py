from pydantic import BaseModel
from typing import Dict, Any, List

class BenchmarkScenarioSchema(BaseModel):
    id: str
    category: str
    name: str
    prospect_context: Dict[str, Any]
    conversation_context: Dict[str, Any]
    objection: Dict[str, str]
    expected_objectives: List[str]
