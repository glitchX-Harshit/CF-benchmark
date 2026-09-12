from pydantic import BaseModel, Field, field_validator
from typing import Literal, List

class OpportunitySignal(BaseModel):
    type: Literal[
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
        "meeting_progression",
        "unclear"
    ]
    evidence_status: Literal[
        "confirmed_by_prospect",
        "created_by_response",
        "seller_claimed",
        "unsupported",
        "not_established"
    ]

    @field_validator("type", "evidence_status", mode="before")
    def lowercase_enums(cls, v):
        if isinstance(v, str):
            return v.lower().strip()
        return v

class SemanticSignals(BaseModel):
    objection_type: Literal[
        "none", "price", "time", "existing_solution", "no_need",
        "lack_of_interest", "authority", "trust", "timing", "competitor", "unclear"
    ] = "unclear"

    acknowledges_prospect: bool = False
    validates_prospect: bool = False
    reduces_resistance: bool = False
    reduces_replacement_fear: bool = False
    contains_product_pitch: bool = False
    pitch_is_premature: bool = False
    contains_unsupported_claim: bool = False
    contains_placeholders: bool = False
    asks_relevant_discovery: bool = False
    asks_multiple_questions: bool = False
    creates_continuation_opening: bool = False
    creates_pain_discovery_opening: bool = False
    creates_gap_discovery_opening: bool = False
    
    likely_prospect_state: Literal[
        "interested", "curious", "engaged", "neutral", "skeptical",
        "defensive", "dismissive", "rushed", "confused", "unclear"
    ] = "unclear"

    cognitive_load: Literal["low", "moderate", "high", "unclear"] = "unclear"
    conversational_cost: Literal["low", "moderate", "high", "unclear"] = "unclear"
    
    opportunities: List[OpportunitySignal] = Field(default_factory=list)

    risk_triggers: List[Literal[
        "defensiveness", "rejection", "loss_of_attention", "premature_pitch",
        "confusion", "cognitive_overload", "scripted_tone", "irrelevant_pitch",
        "pressure", "credibility_loss", "relevance_loss", "shutdown", "none"
    ]] = Field(default_factory=list)

    @field_validator(
        "objection_type", "likely_prospect_state", "cognitive_load", "conversational_cost",
        mode="before"
    )
    def lowercase_enums(cls, v):
        if isinstance(v, str):
            return v.lower().strip()
        return v

    @field_validator("risk_triggers", mode="before")
    def normalize_risk_triggers(cls, v):
        if not v:
            return []
        if isinstance(v, list):
            # lowercase, strip, remove nulls, deduplicate, and sort deterministically
            v = [x.lower().strip() for x in v if isinstance(x, str)]
            v = sorted(list(set(v)))
            return v
        return v

    @field_validator("opportunities", mode="before")
    def normalize_opportunities(cls, v):
        if not v:
            return []
        if isinstance(v, list):
            # deduplicate by type to ensure determinism, and sort
            unique = {}
            for item in v:
                if isinstance(item, dict):
                    t = str(item.get("type", "")).lower().strip()
                    e = str(item.get("evidence_status", "")).lower().strip()
                    if t and t not in unique:
                        unique[t] = {"type": t, "evidence_status": e}
                elif isinstance(item, OpportunitySignal):
                    t = item.type
                    e = item.evidence_status
                    if t not in unique:
                        unique[t] = {"type": t, "evidence_status": e}
            
            # sort by type string
            return [OpportunitySignal(**unique[k]) for k in sorted(unique.keys())]
        return v

    @field_validator(
        "acknowledges_prospect", "validates_prospect", "reduces_resistance",
        "reduces_replacement_fear", "contains_product_pitch", "pitch_is_premature",
        "contains_unsupported_claim", "contains_placeholders", "asks_relevant_discovery",
        "asks_multiple_questions", "creates_continuation_opening", "creates_pain_discovery_opening",
        "creates_gap_discovery_opening",
        mode="before"
    )
    def normalize_bools(cls, v):
        if isinstance(v, str):
            return v.lower().strip() in ("true", "1", "yes")
        return bool(v)
