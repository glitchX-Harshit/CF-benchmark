from pydantic import BaseModel, Field
from typing import Literal, List

class SemanticFlags(BaseModel):
    acknowledges_prospect: bool = False
    validates_prospect: bool = False
    reduces_resistance: bool = False
    reduces_replacement_fear: bool = False
    respects_existing_solution: bool = False
    positions_as_complementary: bool = False
    attacks_existing_solution: bool = False
    relevant_discovery_question: bool = False
    multiple_questions: bool = False
    creates_continuation_opening: bool = False
    creates_current_solution_opening: bool = False
    creates_adoption_opening: bool = False
    creates_pain_opening: bool = False
    creates_gap_opening: bool = False
    contains_product_pitch: bool = False
    pitch_is_premature: bool = False
    pitch_is_relevant: bool = False

class DirectionalInterpretation(BaseModel):
    resistance_tendency: int = Field(0, ge=-100, le=100)
    progression_tendency: int = Field(0, ge=-100, le=100)

class SemanticSignals(BaseModel):
    objection_type: Literal[
        "none",
        "price",
        "time",
        "existing_solution",
        "no_need",
        "lack_of_interest",
        "authority",
        "trust",
        "timing",
        "competitor",
        "unclear"
    ] = "unclear"

    seller_intent: List[Literal[
        "acknowledge",
        "validate",
        "clarify",
        "reduce_resistance",
        "reduce_replacement_fear",
        "respect_existing_solution",
        "position_complementary",
        "discover_current_solution",
        "discover_adoption",
        "discover_pain",
        "discover_gap",
        "qualify",
        "build_relevance",
        "pitch_value",
        "pitch_product",
        "handle_objection",
        "create_continuation",
        "pressure",
        "close",
        "unclear"
    ]] = Field(default_factory=list)

    semantic_signals: SemanticFlags = Field(default_factory=SemanticFlags)

    likely_prospect_state: Literal[
        "interested",
        "curious",
        "engaged",
        "neutral",
        "skeptical",
        "defensive",
        "dismissive",
        "rushed",
        "confused",
        "unclear"
    ] = "unclear"

    directional_interpretation: DirectionalInterpretation = Field(default_factory=DirectionalInterpretation)

    cognitive_load: Literal[
        "low",
        "moderate",
        "high",
        "unclear"
    ] = "unclear"

    conversational_cost: Literal[
        "low",
        "moderate",
        "high",
        "unclear"
    ] = "unclear"

    strengths: List[str] = Field(default_factory=list, max_length=5)
    weaknesses: List[str] = Field(default_factory=list, max_length=5)
    
    opened_opportunities: List[Literal[
        "objection_resolution",
        "current_solution",
        "adoption",
        "workflow",
        "pain_discovery",
        "gap_discovery",
        "curiosity",
        "relevance",
        "qualification",
        "continuation",
        "commercial",
        "meeting_progression"
    ]] = Field(default_factory=list, max_length=6)
    
    weakened_opportunities: List[str] = Field(default_factory=list, max_length=5)
    
    risk_triggers: List[Literal[
        "defensiveness",
        "rejection",
        "loss_of_attention",
        "premature_pitch",
        "confusion",
        "cognitive_overload",
        "scripted_tone",
        "irrelevant_pitch",
        "pressure",
        "credibility_loss",
        "relevance_loss",
        "shutdown",
        "none"
    ]] = Field(default_factory=list, max_length=6)

    semantic_summary: str = ""
    confidence: float = Field(0.0, ge=0.0, le=1.0)
