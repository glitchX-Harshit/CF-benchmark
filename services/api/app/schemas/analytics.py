from pydantic import BaseModel
from typing import Dict

class AnalyticsOverview(BaseModel):
    total_evaluations: int
    average_overall_score: float
    average_response_quality: float
    average_objection_handling: float
    average_forward_momentum: float

class AnalyticsDimensions(BaseModel):
    dimension_averages: Dict[str, float]
