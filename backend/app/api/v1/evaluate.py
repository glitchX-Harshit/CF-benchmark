from fastapi import APIRouter, HTTPException
from typing import Any, Optional, Literal
from cf_engine.models.cold_call import ConversationInput, CFReport
from cf_engine.evaluators.cold_call_engine import ColdCallEngine
from pydantic import BaseModel

router = APIRouter()
engine = ColdCallEngine()

class ColdCallEvaluateRequest(BaseModel):
    conversation: ConversationInput
    seller_response: str
    use_llm: bool = False
    analysis_mode: Literal["deterministic", "hybrid"] = "deterministic"

class ColdCallEvaluateResponse(BaseModel):
    evaluation_id: str
    report: CFReport

@router.post("/cold-call", response_model=ColdCallEvaluateResponse)
def evaluate_cold_call(request: ColdCallEvaluateRequest):
    try:
        report = engine.evaluate(
            request.conversation, 
            request.seller_response,
            use_llm=request.use_llm or request.analysis_mode == "hybrid"
        )
        return ColdCallEvaluateResponse(
            evaluation_id="eval-temp-id",
            report=report
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
