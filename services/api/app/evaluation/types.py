from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class ScenarioInput(BaseModel):
    industry: str
    prospect_role: str
    company_context: Dict[str, Any]
    prospect_context: Dict[str, Any]
    objection: str
    hidden_concern: List[str]
    desired_outcome: List[str]
    expected_strategy: List[str]

class DimensionResult(BaseModel):
    dimension: str
    score: float
    reasoning: str
    evidence: str

class EvaluationResult(BaseModel):
    overall_score: float
    response_quality_score: float
    objection_handling_score: float
    forward_momentum_score: float
    dimensions: List[DimensionResult]
    strengths: List[str]
    weaknesses: List[str]
    missed_opportunities: List[str]
    recommended_strategy: str
