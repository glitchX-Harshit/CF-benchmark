from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class RubricScore(BaseModel):
    rubric_id: str
    score: int
    max_score: int
    reason: str
    evidence: List[str] = Field(default_factory=list)
    confidence: float

class EvaluationResult(BaseModel):
    overall_score: float
    rubrics: Dict[str, RubricScore]
    strengths: List[str] = Field(default_factory=list)
    weaknesses: List[str] = Field(default_factory=list)
    recommended_strategy: List[str] = Field(default_factory=list)
    evaluator_version: str

class BenchmarkScenario(BaseModel):
    id: str
    category: str
    prospect: Dict[str, Any]
    context: Dict[str, Any]
    objection: Dict[str, str]
    evaluation_targets: List[str]
