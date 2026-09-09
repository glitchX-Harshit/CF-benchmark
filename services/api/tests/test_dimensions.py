from app.evaluation.dimensions import score_objection_recognition, score_empathy
from app.evaluation.types import ScenarioInput

def test_objection_recognition(sample_scenario):
    response = "I hear that it costs too much."
    res = score_objection_recognition(response, sample_scenario)
    assert res.score > 0

def test_empathy(sample_scenario):
    response = "I completely understand why you feel that way."
    res = score_empathy(response, sample_scenario)
    assert res.score > 0
