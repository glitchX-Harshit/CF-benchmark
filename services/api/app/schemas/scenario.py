from pydantic import BaseModel, ConfigDict
from typing import List, Dict, Any, Optional
import uuid
from datetime import datetime
from app.models.scenario import SalesStage

class ScenarioBase(BaseModel):
    name: str
    description: str
    industry: str
    sales_stage: SalesStage
    prospect_role: str
    company_context: Dict[str, Any]
    prospect_context: Dict[str, Any]
    objection: str
    hidden_concern: List[str]
    desired_outcome: List[str]
    expected_strategy: List[str]

class ScenarioCreate(ScenarioBase):
    pass

class ScenarioUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    industry: Optional[str] = None
    sales_stage: Optional[SalesStage] = None
    prospect_role: Optional[str] = None
    company_context: Optional[Dict[str, Any]] = None
    prospect_context: Optional[Dict[str, Any]] = None
    objection: Optional[str] = None
    hidden_concern: Optional[List[str]] = None
    desired_outcome: Optional[List[str]] = None
    expected_strategy: Optional[List[str]] = None

class ScenarioResponse(ScenarioBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
