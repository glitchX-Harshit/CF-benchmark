from cf_engine.llm.schemas import SemanticSignals

SCORING_WEIGHTS = {
    "acknowledges_prospect": 8,
    "validates_prospect": 6,
    "reduces_resistance": 10,
    "reduces_replacement_fear": 10,
    "respects_existing_solution": 8,
    "attacks_existing_solution": -15,
    "relevant_discovery": 12,
    "gap_discovery": 8,
    "premature_pitch": -12,
    "multiple_questions": -5,
    "high_cognitive_load": -6,
}

def calculate_deterministic_score(
    objective_signals: dict,
    semantic: SemanticSignals,
) -> dict:
    
    # Start with base scores that can be affected by the semantic signals
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

    if semantic.respects_existing_solution:
        strategic_opportunity += SCORING_WEIGHTS["respects_existing_solution"]
        direction += 8

    if semantic.asks_relevant_discovery:
        strategic_opportunity += SCORING_WEIGHTS["relevant_discovery"]
        direction += 14

    if semantic.creates_gap_discovery_opening:
        strategic_opportunity += SCORING_WEIGHTS["gap_discovery"]
        direction += 8

    if semantic.attacks_existing_solution:
        response_quality += SCORING_WEIGHTS["attacks_existing_solution"]
        direction -= 15

    if semantic.pitch_is_premature:
        strategic_opportunity += SCORING_WEIGHTS["premature_pitch"]
        direction -= 12

    if semantic.asks_multiple_questions:
        direction += SCORING_WEIGHTS["multiple_questions"]

    if semantic.cognitive_load == "high":
        response_quality += SCORING_WEIGHTS["high_cognitive_load"]
        direction -= 5
        
    # Extra rules based on spec to match some more robust semantic qualities
    if semantic.creates_relevance_opening:
        strategic_opportunity += 10
        direction += 8
        
    if semantic.tone in ["defensive", "aggressive", "pressuring", "dismissive"]:
        response_quality -= 15
        direction -= 20
        
    if semantic.tone in ["reassuring", "calm", "curious"]:
        response_quality += 10
        direction += 5
        
    # Clamp bounds
    response_quality = max(0, min(100, response_quality))
    strategic_opportunity = max(0, min(100, strategic_opportunity))
    direction = max(-100, min(100, direction))

    return {
        "response_quality_score": response_quality,
        "strategic_opportunity_score": strategic_opportunity,
        "conversation_direction_score": direction
    }
