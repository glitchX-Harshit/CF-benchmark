import pytest
from pydantic import ValidationError
from cf_engine.models.cold_call import ConversationInput, CurrentState
from cf_engine.llm.schemas import SemanticSignals, OpportunitySignal
from cf_engine.evaluators.semantic_evaluator import calculate_deterministic_score
from cf_engine.evaluators.cold_call_engine import ColdCallEngine

def test_semantic_schema_validation():
    # Valid
    signals = SemanticSignals(objection_type="price", likely_prospect_state="interested")
    assert signals.objection_type == "price"
    assert signals.cognitive_load == "unclear"
    
    # Invalid enum value
    with pytest.raises(ValidationError):
        SemanticSignals(likely_prospect_state="angry_shouting")

    # Array normalization: deduplication and sorting
    signals2 = SemanticSignals(
        risk_triggers=["premature_pitch", "defensiveness", "premature_pitch", "none"],
        opportunities=[
            OpportunitySignal(type="workflow", evidence_status="seller_claimed"),
            OpportunitySignal(type="adoption", evidence_status="confirmed_by_prospect"),
            OpportunitySignal(type="workflow", evidence_status="unsupported")
        ]
    )
    assert signals2.risk_triggers == ["defensiveness", "none", "premature_pitch"]
    # workflow deduplicated, adoption sorted first
    assert len(signals2.opportunities) == 2
    assert signals2.opportunities[0].type == "adoption"
    assert signals2.opportunities[1].type == "workflow"


def test_deterministic_scoring_rules():
    objective_signals = {"contains_placeholders": False, "contains_meeting_request": False, "question_count": 0}
    
    semantic = SemanticSignals()
    scores = calculate_deterministic_score(objective_signals, semantic)
    assert scores["response_quality_score"] == 50
    assert scores["conversation_direction_score"] == 0
    
    semantic.acknowledges_prospect = True
    scores = calculate_deterministic_score(objective_signals, semantic)
    assert scores["response_quality_score"] == 58
    assert scores["conversation_direction_score"] == 6
    
    semantic.cognitive_load = "high"
    scores = calculate_deterministic_score(objective_signals, semantic)
    assert scores["response_quality_score"] == 50
    assert scores["conversation_direction_score"] == -2
    
    semantic.pitch_is_premature = True
    scores = calculate_deterministic_score(objective_signals, semantic)
    assert scores["conversation_direction_score"] == -17
    
    # Test unconfirmed opportunities do NOT add score
    semantic.opportunities = [OpportunitySignal(type="workflow", evidence_status="seller_claimed")]
    scores1 = calculate_deterministic_score(objective_signals, semantic)
    semantic.opportunities = [OpportunitySignal(type="workflow", evidence_status="created_by_response")]
    scores2 = calculate_deterministic_score(objective_signals, semantic)
    
    assert scores2["strategic_opportunity_score"] > scores1["strategic_opportunity_score"]


def test_regression_deterministic_20_times(monkeypatch):
    engine = ColdCallEngine()
    conv = ConversationInput()
    response = "That makes sense. Can we discuss your [problem area] for 5 minutes?"
    
    # We will simulate the LLM returning slightly out-of-order JSON 
    # to ensure our normalizers make it strictly identical in the final result.
    def mock_interpret(*args, **kwargs):
        # We mutate the order to simulate LLM non-determinism in arrays
        import random
        risks = ["defensiveness", "premature_pitch"]
        random.shuffle(risks)
        
        opps = [
            OpportunitySignal(type="workflow", evidence_status="seller_claimed"),
            OpportunitySignal(type="gap_discovery", evidence_status="created_by_response")
        ]
        random.shuffle(opps)
        
        return SemanticSignals(
            objection_type="price",
            acknowledges_prospect=True,
            contains_placeholders=True,
            risk_triggers=risks,
            opportunities=opps,
            likely_prospect_state="skeptical",
            cognitive_load="moderate",
            conversational_cost="low"
        )
        
    monkeypatch.setattr(engine.llm, "interpret_response", mock_interpret)
    
    baseline = engine.evaluate(conv, response, use_llm=True)
    
    for _ in range(20):
        report = engine.evaluate(conv, response, use_llm=True)
        assert report.response_quality["score"] == baseline.response_quality["score"]
        assert report.strategic_opportunity["score"] == baseline.strategic_opportunity["score"]
        assert report.conversation_direction["score"] == baseline.conversation_direction["score"]
        assert report.final.cf_grade == baseline.final.cf_grade
        assert report.metadata.analysis_mode == "hybrid"


def test_cross_scenario_contamination(monkeypatch):
    engine = ColdCallEngine()
    conv = ConversationInput(current_state=CurrentState(objection="We have no budget right now", prospect_role="Director"))
    response = "I understand budget is tight. What if it pays for itself?"
    
    def mock_interpret(*args, **kwargs):
        return SemanticSignals(
            objection_type="budget",
            opportunities=[OpportunitySignal(type="commercial", evidence_status="created_by_response")]
        )
        
    monkeypatch.setattr(engine.llm, "interpret_response", mock_interpret)
    report = engine.evaluate(conv, response, use_llm=True)
    
    # Assert that no default salesforce text is present in the report
    report_json = report.model_dump_json().lower()
    assert "salesforce" not in report_json
    assert "crm replacement" not in report_json


def test_contradiction_check(monkeypatch):
    engine = ColdCallEngine()
    conv = ConversationInput()
    # High cognitive load, placeholder, meeting request
    response = "Let's meet tomorrow. I want to show you [X%] ROI on [problem area]."
    
    def mock_interpret(*args, **kwargs):
        return SemanticSignals(
            likely_prospect_state="interested",
            cognitive_load="high",
            contains_placeholders=True,
            contains_unsupported_claim=True,
            risk_triggers=["rejection", "credibility_loss"]
        )
    monkeypatch.setattr(engine.llm, "interpret_response", mock_interpret)
    report = engine.evaluate(conv, response, use_llm=True)
    
    # Because of risks and penalties, direction should be severely penalized.
    # The verdict MUST NOT say "Strong cold-call response..."
    assert report.final.verdict != "Strong cold-call response. It creates multiple useful paths without forcing a pitch or adding unnecessary conversational cost."
    assert "major high-severity risks" in report.final.verdict or report.conversation_direction["score"] < 70
