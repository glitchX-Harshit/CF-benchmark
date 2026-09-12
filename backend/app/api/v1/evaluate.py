from fastapi import APIRouter, HTTPException, Depends
from typing import Any, Optional, Literal
from cf_engine.models.cold_call import ConversationInput, CFReport
from cf_engine.evaluators.cold_call_engine import ColdCallEngine
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from ...core.database import get_db
from ...models.evaluation import Evaluation

load_dotenv() # Load variables from .env into os.environ

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
def evaluate_cold_call(request: ColdCallEvaluateRequest, db: Session = Depends(get_db)):
    try:
        report = engine.evaluate(
            request.conversation, 
            request.seller_response,
            use_llm=request.use_llm or request.analysis_mode == "hybrid"
        )
        
        # Save to DB
        db_eval = Evaluation(
            prospect_role=request.conversation.current_state.prospect_role if request.conversation.current_state else "Unknown",
            objection_text=request.conversation.current_state.objection if request.conversation.current_state else "Unknown",
            seller_response=request.seller_response,
            final_score=report.final.cf_score,
            response_quality=report.response_quality["score"],
            strategic_opportunity=report.strategic_opportunity["score"],
            direction_score=report.conversation_direction["score"],
            report_data=report.model_dump()
        )
        db.add(db_eval)
        db.commit()
        db.refresh(db_eval)
        
        return ColdCallEvaluateResponse(
            evaluation_id=db_eval.id,
            report=report
        )
    except Exception as e:
        if str(e) == "LLM_QUOTA_REACHED":
            raise HTTPException(status_code=429, detail="LLM Quota or Rate Limit Reached. Please try again later or upgrade your API key.")
        raise HTTPException(status_code=500, detail=str(e))
