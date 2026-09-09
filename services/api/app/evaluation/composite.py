from typing import List
from .types import DimensionResult

def calculate_response_quality(dimensions: List[DimensionResult]) -> float:
    weights = {"relevance": 0.3, "value_articulation": 0.3, "credibility": 0.2, "differentiation": 0.2}
    score = 0.0
    for dim in dimensions:
        if dim.dimension in weights:
            score += (dim.score / 5.0) * 100 * weights[dim.dimension]
    return score

def calculate_objection_handling(dimensions: List[DimensionResult]) -> float:
    weights = {"objection_recognition": 0.3, "objection_coverage": 0.3, "empathy": 0.2, "persuasion": 0.2}
    score = 0.0
    for dim in dimensions:
        if dim.dimension in weights:
            score += (dim.score / 5.0) * 100 * weights[dim.dimension]
    return score

def calculate_forward_momentum(dimensions: List[DimensionResult]) -> float:
    weights = {"next_step_quality": 0.6, "resistance_risk": 0.4}
    score = 0.0
    for dim in dimensions:
        if dim.dimension in weights:
            score += (dim.score / 5.0) * 100 * weights[dim.dimension]
    return score
