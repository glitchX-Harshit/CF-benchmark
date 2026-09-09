from pydantic import BaseModel, ConfigDict
from typing import List, Dict, Any, Optional
import uuid
from datetime import datetime

class EvaluationCreate(BaseModel):
    scenario_id: uuid.UUID
    seller_response: str

class EvaluationPreviewRequest(BaseModel):
    prospect_context: Optional[str] = None
    conversation_context: Optional[str] = None
    objection: str
    seller_response: str
    sales_stage: str
    industry: Optional[str] = None
    company_context: Optional[str] = None

class EvaluationPreviewResponse(BaseModel):
    overall_score: float
    response_quality_score: float
    objection_handling_score: float
    forward_momentum_score: float
    evaluation_version: str
    strengths: List[str]
    weaknesses: List[str]
    missed_opportunities: List[str]
    recommended_strategy: str
    dimensions: List[Dict[str, Any]]

class DimensionScoreResponse(BaseModel):
    id: uuid.UUID
    dimension: str
    score: float
    reasoning: str
    evidence: str

    model_config = ConfigDict(from_attributes=True)

class EvaluationResponse(BaseModel):
    id: uuid.UUID
    scenario_id: uuid.UUID
    seller_response: str
    overall_score: float
    response_quality_score: float
    objection_handling_score: float
    forward_momentum_score: float
    evaluation_version: str
    strengths: List[str]
    weaknesses: List[str]
    missed_opportunities: List[str]
    recommended_strategy: str
    created_at: datetime
    scores: List[DimensionScoreResponse]

    model_config = ConfigDict(from_attributes=True)
