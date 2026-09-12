import pytest
from pydantic import ValidationError
from cf_engine.models.cold_call import ConversationInput
from cf_engine.llm.schemas import SemanticSignals
from cf_engine.evaluators.semantic_evaluator import calculate_deterministic_score
from cf_engine.evaluators.cold_call_engine import ColdCallEngine

def test_semantic_schema_validation():
    # Valid
    signals = SemanticSignals(objection_type="price", likely_prospect_state="interested")
    assert signals.objection_type == "price"
    
    # Missing optional fields will use defaults
    assert signals.tone == "unclear"
    
    # Invalid enum value
    with pytest.raises(ValidationError):
        SemanticSignals(tone="angry_shouting")

def test_deterministic_scoring_rules():
    objective_signals = {}
    
    # Base neutral
    semantic = SemanticSignals()
    scores = calculate_deterministic_score(objective_signals, semantic)
    assert scores["response_quality_score"] == 50
    assert scores["conversation_direction_score"] == 0
    
    # Acknowledges prospect (+8 quality, +6 direction)
    semantic.acknowledges_prospect = True
    scores = calculate_deterministic_score(objective_signals, semantic)
    assert scores["response_quality_score"] == 58
    assert scores["conversation_direction_score"] == 6
    
    # Adds high cognitive load (-6 quality, -5 direction)
    semantic.cognitive_load = "high"
    scores = calculate_deterministic_score(objective_signals, semantic)
    assert scores["response_quality_score"] == 52
    assert scores["conversation_direction_score"] == 1
    
    # Attacking existing solution (-15 direction)
    semantic.attacks_existing_solution = True
    scores = calculate_deterministic_score(objective_signals, semantic)
    assert scores["conversation_direction_score"] == -14
    
    # Clamping tests
    semantic.tone = "defensive"  # heavily negative
    semantic.attacks_existing_solution = True
    semantic.pitch_is_premature = True
    scores = calculate_deterministic_score(objective_signals, semantic)
    assert scores["conversation_direction_score"] >= -100

def test_engine_fallback():
    engine = ColdCallEngine()
    conv = ConversationInput()
    # Explicitly asking for LLM but we have no API key so fallback happens
    # Well actually, if the API request fails (which it will without key/mock), it catches and falls back.
    report = engine.evaluate(conv, "Okay.", use_llm=True)
    assert report.metadata.analysis_mode == "deterministic_fallback"
    assert report.metadata.fallback_used == True
    
    # And if not requested, it uses deterministic
    report = engine.evaluate(conv, "Okay.", use_llm=False)
    assert report.metadata.analysis_mode == "deterministic"

def test_objective_parsing():
    engine = ColdCallEngine()
    conv = ConversationInput()
    report = engine.evaluate(conv, "Is this a platform solution?")
    assert report.response_cost.word_count == 5
    assert len(report.risks) > 0 # Premature pitch risk due to 'platform solution'
    
def test_golden_case_strong_salesforce_handling(monkeypatch):
    engine = ColdCallEngine()
    conv = ConversationInput()
    response = "Totally fair — I'm not suggesting you replace Salesforce. We usually help teams get more value from the tools they already use. Out of curiosity, are your reps consistently using Salesforce the way you want them to?"
    
    # Mock LLM response
    def mock_interpret(*args, **kwargs):
        return SemanticSignals(
            objection_type="existing_solution",
            acknowledges_prospect=True,
            validates_prospect=True,
            reduces_resistance=True,
            reduces_replacement_fear=True,
            respects_existing_solution=True,
            asks_relevant_discovery=True,
            creates_gap_discovery_opening=True,
            contains_product_pitch=True,
            pitch_is_premature=False,
            likely_prospect_state="curious",
            cognitive_load="moderate",
            conversational_cost=58
        )
    monkeypatch.setattr(engine.llm, "interpret_response", mock_interpret)
    
    # Test hybrid mode
    report = engine.evaluate(conv, response, use_llm=True)
    assert report.response_cost.word_count == 37
    assert 70 <= report.response_quality["score"] <= 95
    assert 70 <= report.strategic_opportunity["score"] <= 95
    assert report.final.cf_grade in ["A", "A-", "B+"]
    
def test_golden_case_premature_pitch():
    engine = ColdCallEngine()
    conv = ConversationInput()
    response = "Makes sense. Our platform is an AI-powered sales intelligence solution that integrates with Salesforce and helps companies improve visibility, rep productivity, forecasting, pipeline management, coaching, analytics and much more."
    report = engine.evaluate(conv, response, use_llm=False)
    assert report.conversation_direction["score"] <= 10
    assert report.final.cf_grade in ["C", "C+", "C-", "D", "F"]

def test_golden_case_one_word():
    engine = ColdCallEngine()
    conv = ConversationInput()
    report = engine.evaluate(conv, "Okay.", use_llm=False)
    assert report.final.cf_grade in ["C", "C+", "C-", "D"]
    assert report.conversation_direction["score"] < 0
