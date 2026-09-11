from typing import Dict, Any
from cf_engine.models.models import BenchmarkScenario, EvaluationResult, RubricScore

class DummyEvaluator:
    """
    A simple deterministic evaluator for the initial vertical slice.
    In real usage, this would invoke a Layer 1 (deterministic) and Layer 2 (LLM) pipeline.
    """
    def __init__(self, version: str = "cf-eval-0.1.0"):
        self.version = version

    def evaluate(self, scenario: BenchmarkScenario, response: str) -> EvaluationResult:
        # A mock deterministic evaluation logic for the demo
        length = len(response)
        objection_coverage_score = min(5, max(1, length // 20))
        empathy_score = 4 if "understand" in response.lower() else 2
        
        overall = (objection_coverage_score * 20 + empathy_score * 20) / 2
        
        rubrics = {
            "objection_coverage": RubricScore(
                rubric_id="objection_coverage",
                score=objection_coverage_score,
                max_score=5,
                reason="Response addresses some parts of the objection based on length heuristic.",
                confidence=0.8
            ),
            "empathy": RubricScore(
                rubric_id="empathy",
                score=empathy_score,
                max_score=5,
                reason="Detected empathy keywords." if empathy_score > 2 else "No clear empathy keywords detected.",
                confidence=0.9
            )
        }
        
        return EvaluationResult(
            overall_score=overall,
            rubrics=rubrics,
            strengths=["Attempted to answer" if length > 10 else "N/A"],
            weaknesses=["Too short" if length < 50 else "N/A"],
            recommended_strategy=["Ask more discovery questions."],
            evaluator_version=self.version
        )
