from .types import ScenarioInput, EvaluationResult, DimensionResult
from .dimensions import (
    score_objection_recognition, score_empathy, score_relevance,
    score_objection_coverage, score_value_articulation, score_differentiation,
    score_credibility, score_persuasion, score_resistance_risk, score_next_step_quality
)
from .composite import (
    calculate_response_quality, calculate_objection_handling, calculate_forward_momentum
)

class EvaluationEngine:
    def __init__(self, version: str = "1.0.0"):
        self.version = version

    def evaluate(self, response: str, scenario: ScenarioInput) -> EvaluationResult:
        dimensions = [
            score_objection_recognition(response, scenario),
            score_empathy(response, scenario),
            score_relevance(response, scenario),
            score_objection_coverage(response, scenario),
            score_value_articulation(response, scenario),
            score_differentiation(response, scenario),
            score_credibility(response, scenario),
            score_persuasion(response, scenario),
            score_resistance_risk(response, scenario),
            score_next_step_quality(response, scenario)
        ]
        
        rq_score = calculate_response_quality(dimensions)
        oh_score = calculate_objection_handling(dimensions)
        fm_score = calculate_forward_momentum(dimensions)
        
        overall = (rq_score + oh_score + fm_score) / 3.0
        
        strengths = [d.dimension for d in dimensions if d.score >= 4.0]
        weaknesses = [d.dimension for d in dimensions if d.score <= 2.0]
        
        return EvaluationResult(
            overall_score=overall,
            response_quality_score=rq_score,
            objection_handling_score=oh_score,
            forward_momentum_score=fm_score,
            dimensions=dimensions,
            strengths=strengths if strengths else ["Adequate response overall"],
            weaknesses=weaknesses if weaknesses else ["No major weaknesses"],
            missed_opportunities=["Could be more specific to prospect context"],
            recommended_strategy="Focus on tying the value directly back to the hidden concerns."
        )
