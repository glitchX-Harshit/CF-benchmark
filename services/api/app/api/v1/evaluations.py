from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select
from typing import List
import uuid

from app.api.deps import get_db
from app.models.scenario import Scenario
from app.models.evaluation import Evaluation, DimensionScore
from app.schemas.evaluation import EvaluationCreate, EvaluationResponse, EvaluationPreviewRequest, EvaluationPreviewResponse
from app.schemas.common import PaginatedResponse
from app.evaluation.engine import EvaluationEngine
from app.evaluation.types import ScenarioInput

router = APIRouter()
engine = EvaluationEngine()

@router.post("", response_model=EvaluationResponse)
async def create_evaluation(
    eval_in: EvaluationCreate,
    db: AsyncSession = Depends(get_db)
):
    scenario_query = select(Scenario).where(Scenario.id == eval_in.scenario_id)
    scenario_result = await db.execute(scenario_query)
    scenario = scenario_result.scalar_one_or_none()
    
    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario not found")
        
    scenario_input = ScenarioInput(
        industry=scenario.industry,
        prospect_role=scenario.prospect_role,
        company_context=scenario.company_context,
        prospect_context=scenario.prospect_context,
        objection=scenario.objection,
        hidden_concern=scenario.hidden_concern,
        desired_outcome=scenario.desired_outcome,
        expected_strategy=scenario.expected_strategy
    )
    
    eval_result = engine.evaluate(eval_in.seller_response, scenario_input)
    
    db_evaluation = Evaluation(
        scenario_id=scenario.id,
        seller_response=eval_in.seller_response,
        overall_score=eval_result.overall_score,
        response_quality_score=eval_result.response_quality_score,
        objection_handling_score=eval_result.objection_handling_score,
        forward_momentum_score=eval_result.forward_momentum_score,
        evaluation_version=engine.version,
        raw_result={},
        strengths=eval_result.strengths,
        weaknesses=eval_result.weaknesses,
        missed_opportunities=eval_result.missed_opportunities,
        recommended_strategy=eval_result.recommended_strategy
    )
    db.add(db_evaluation)
    await db.flush()
    
    for dim in eval_result.dimensions:
        db_score = DimensionScore(
            evaluation_id=db_evaluation.id,
            dimension=dim.dimension,
            score=dim.score,
            reasoning=dim.reasoning,
            evidence=dim.evidence
        )
        db.add(db_score)
        
    await db.commit()
    
    eval_query = select(Evaluation).options(selectinload(Evaluation.scores)).where(Evaluation.id == db_evaluation.id)
    final_result = await db.execute(eval_query)
    
    return final_result.scalar_one()

@router.post("/preview", response_model=EvaluationPreviewResponse)
async def preview_evaluation(
    eval_in: EvaluationPreviewRequest,
):
    scenario_input = ScenarioInput(
        industry=eval_in.industry or "Unknown",
        prospect_role="Unknown",
        company_context={"info": eval_in.company_context} if eval_in.company_context else {},
        prospect_context={"info": eval_in.prospect_context} if eval_in.prospect_context else {},
        objection=eval_in.objection,
        hidden_concern=[],
        desired_outcome=[],
        expected_strategy=[]
    )
    
    eval_result = engine.evaluate(eval_in.seller_response, scenario_input)
    
    return EvaluationPreviewResponse(
        overall_score=eval_result.overall_score,
        response_quality_score=eval_result.response_quality_score,
        objection_handling_score=eval_result.objection_handling_score,
        forward_momentum_score=eval_result.forward_momentum_score,
        evaluation_version=engine.version,
        strengths=eval_result.strengths,
        weaknesses=eval_result.weaknesses,
        missed_opportunities=eval_result.missed_opportunities,
        recommended_strategy=eval_result.recommended_strategy,
        dimensions=[
            {
                "dimension": dim.dimension,
                "score": dim.score,
                "reasoning": dim.reasoning,
                "evidence": dim.evidence
            } for dim in eval_result.dimensions
        ]
    )

@router.get("", response_model=PaginatedResponse[EvaluationResponse])
async def list_evaluations(
    page: int = 1,
    size: int = 50,
    db: AsyncSession = Depends(get_db)
):
    offset = (page - 1) * size
    query = select(Evaluation).options(selectinload(Evaluation.scores)).offset(offset).limit(size)
    result = await db.execute(query)
    evaluations = result.scalars().all()
    
    return PaginatedResponse(
        items=list(evaluations),
        total=len(evaluations),
        page=page,
        size=size
    )

@router.get("/{evaluation_id}", response_model=EvaluationResponse)
async def get_evaluation(
    evaluation_id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
):
    query = select(Evaluation).options(selectinload(Evaluation.scores)).where(Evaluation.id == evaluation_id)
    result = await db.execute(query)
    evaluation = result.scalar_one_or_none()
    
    if not evaluation:
        raise HTTPException(status_code=404, detail="Evaluation not found")
        
    return evaluation
