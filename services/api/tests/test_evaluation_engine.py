from app.evaluation.engine import EvaluationEngine
from app.evaluation.types import ScenarioInput

def test_evaluation_engine(sample_scenario):
    engine = EvaluationEngine()
    response = "I understand budget is tight. Our solution actually provides a 2x ROI within 6 months, reducing deployment costs."
    result = engine.evaluate(response, sample_scenario)
    assert result.overall_score > 0
    assert len(result.dimensions) == 10
