from app.evaluation.composite import calculate_response_quality
from app.evaluation.types import DimensionResult

def test_calculate_response_quality():
    dims = [
        DimensionResult(dimension="relevance", score=5.0, reasoning="", evidence=""),
        DimensionResult(dimension="value_articulation", score=5.0, reasoning="", evidence="")
    ]
    score = calculate_response_quality(dims)
    assert score > 0
