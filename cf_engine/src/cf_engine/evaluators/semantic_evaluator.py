from cf_engine.llm.schemas import SemanticSignals

SCORING_WEIGHTS = {
    "acknowledges_prospect": 8,
    "validates_prospect": 6,
    "reduces_resistance": 10,
    "reduces_replacement_fear": 10,
    "relevant_discovery": 12,
    "gap_discovery": 8,
    "premature_pitch": -15,
    "multiple_questions": -5,
    "high_cognitive_load": -8,
    "placeholder_penalty": -15,
    "unsupported_claim_penalty": -20,
    "meeting_request_penalty": -10,
}

def calculate_deterministic_score(
    objective_signals: dict,
    semantic: SemanticSignals,
) -> dict:
    
    response_quality = 50
    strategic_opportunity = 50
    direction = 0

    if semantic.acknowledges_prospect:
        response_quality += SCORING_WEIGHTS["acknowledges_prospect"]
        direction += 6

    if semantic.validates_prospect:
        response_quality += SCORING_WEIGHTS["validates_prospect"]
        direction += 5

    if semantic.reduces_resistance:
        response_quality += SCORING_WEIGHTS["reduces_resistance"]
        direction += 10

    if semantic.reduces_replacement_fear:
        response_quality += SCORING_WEIGHTS["reduces_replacement_fear"]
        direction += 12

    if semantic.asks_relevant_discovery:
        strategic_opportunity += SCORING_WEIGHTS["relevant_discovery"]
        direction += 14

    if semantic.creates_gap_discovery_opening:
        strategic_opportunity += SCORING_WEIGHTS["gap_discovery"]
        direction += 8

    if semantic.pitch_is_premature:
        strategic_opportunity += SCORING_WEIGHTS["premature_pitch"]
        direction -= 15

    # Check objective flags for penalties
    if objective_signals.get("contains_placeholders") or semantic.contains_placeholders:
        response_quality += SCORING_WEIGHTS["placeholder_penalty"]
        direction += SCORING_WEIGHTS["placeholder_penalty"]

    if semantic.contains_unsupported_claim:
        response_quality += SCORING_WEIGHTS["unsupported_claim_penalty"]
        direction += SCORING_WEIGHTS["unsupported_claim_penalty"]

    if objective_signals.get("contains_meeting_request"):
        direction += SCORING_WEIGHTS["meeting_request_penalty"]

    if objective_signals.get("question_count", 0) > 1 or semantic.asks_multiple_questions:
        direction += SCORING_WEIGHTS["multiple_questions"]

    if semantic.cognitive_load == "high":
        response_quality += SCORING_WEIGHTS["high_cognitive_load"]
        direction -= 8
        
    if semantic.conversational_cost == "high":
        direction -= 5

    # Tone equivalent mapped from likely_prospect_state and risks
    if semantic.likely_prospect_state in ["defensive", "dismissive", "skeptical"]:
        response_quality -= 15
        direction -= 20
        
    if semantic.likely_prospect_state in ["interested", "curious"]:
        response_quality += 10
        direction += 10

    if "defensiveness" in semantic.risk_triggers or "pressure" in semantic.risk_triggers or "rejection" in semantic.risk_triggers:
        direction -= 15

    # Opportunities processing
    # Only confirmed_by_prospect and created_by_response can contribute
    valid_opportunities = 0
    for opp in semantic.opportunities:
        if opp.evidence_status in ["confirmed_by_prospect", "created_by_response"]:
            valid_opportunities += 1
            
    strategic_opportunity += (valid_opportunities * 8)
    direction += (valid_opportunities * 5)

    # Clamp bounds
    response_quality = max(0, min(100, response_quality))
    strategic_opportunity = max(0, min(100, strategic_opportunity))
    direction = max(-100, min(100, direction))

    return {
        "response_quality_score": response_quality,
        "strategic_opportunity_score": strategic_opportunity,
        "conversation_direction_score": direction
    }
