from fastapi import APIRouter, HTTPException
from typing import Any
from ...schemas.evaluation import EvaluationRequest, EvaluationResponse
from cf_engine.evaluators.base import DummyEvaluator
from cf_engine.models.models import BenchmarkScenario

router = APIRouter()

evaluator = DummyEvaluator()

@router.post("/", response_model=EvaluationResponse)
def evaluate_response(request: EvaluationRequest):
    scenario = BenchmarkScenario(
        id=request.scenario_id,
        category="mock",
        prospect={"role": "VP Sales"},
        context={"stage": "discovery"},
        objection={"text": "We already have a solution."},
        evaluation_targets=[]
    )
    
    result = evaluator.evaluate(scenario=scenario, response=request.response)
    
    # Normally we would persist this result to DB here via repository
    return EvaluationResponse(
        id="eval-mock-id",
        scenario_id=request.scenario_id,
        result=result.model_dump(),
        overall_score=result.overall_score
    )
