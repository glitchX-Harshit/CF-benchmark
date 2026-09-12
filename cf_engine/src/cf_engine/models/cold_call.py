from pydantic import BaseModel, Field
from typing import List, Optional, Literal, Dict, Any

class Message(BaseModel):
    speaker: Literal["prospect", "seller"]
    text: str

class CurrentState(BaseModel):
    prospect_role: str = ""
    company_context: Optional[str] = None
    known_problem: Optional[str] = None
    known_solution: Optional[str] = None
    objection: Optional[str] = None
    engagement_level: Literal["unknown", "low", "medium", "high"] = "unknown"
    resistance_level: Literal["unknown", "low", "medium", "high"] = "unknown"
    urgency: Literal["unknown", "low", "medium", "high"] = "unknown"
    stage: Literal["opening", "problem_discovery", "solution_discussion", "objection", "qualification", "commercial", "closing"] = "opening"

class ConversationInput(BaseModel):
    previous_messages: List[Message] = Field(default_factory=list)
    current_state: Optional[CurrentState] = None

class DirectionItem(BaseModel):
    direction: str
    likelihood_tendency: Literal["LOW", "MEDIUM", "HIGH"]
    explanation: str

class OpportunityItem(BaseModel):
    type: str
    strength: int # 0-100
    reason: str
    reachable_direction: str

class OpportunitySurface(BaseModel):
    opened: List[OpportunityItem] = Field(default_factory=list)
    missed: List[OpportunityItem] = Field(default_factory=list)
    weakened: List[OpportunityItem] = Field(default_factory=list)

class RiskItem(BaseModel):
    type: str
    severity: Literal["low", "medium", "high"]
    reason: str

class ResponseCost(BaseModel):
    word_count: int
    estimated_seconds: float
    cognitive_load: int # 0-100
    conversational_cost: int # 0-100

class LikelyProspectEffect(BaseModel):
    engagement: Literal["LOW", "MEDIUM", "HIGH"]
    curiosity: Literal["LOW", "MEDIUM", "HIGH"]
    resistance: Literal["LOW", "MEDIUM", "HIGH"]
    trust: Literal["LOW", "MEDIUM", "HIGH"]
    relevance: Literal["LOW", "MEDIUM", "HIGH"]
    continuation: Literal["LOW", "MEDIUM", "HIGH"]

class LikelyReaction(BaseModel):
    label: str
    explanation: str

class FinalGrade(BaseModel):
    cf_grade: str
    cf_score: int
    direction: str
    verdict: str

class CFReportMetadata(BaseModel):
    analysis_mode: Literal["deterministic", "hybrid", "deterministic_fallback"] = "deterministic"
    semantic_source: str = "deterministic"
    llm_used: bool = False
    fallback_used: bool = False

class CFReport(BaseModel):
    seller_response: str
    response_quality: Dict[str, Any] # score and label
    strategic_opportunity: Dict[str, Any]
    conversation_direction: Dict[str, Any]
    direction_visual: str
    likely_prospect_effect: LikelyProspectEffect
    likely_reaction: LikelyReaction
    possible_directions: List[DirectionItem]
    opportunity_surface: OpportunitySurface
    risks: List[RiskItem]
    response_cost: ResponseCost
    resilience: Dict[str, Any] # score and explanation
    final: FinalGrade
    metadata: CFReportMetadata = Field(default_factory=CFReportMetadata)