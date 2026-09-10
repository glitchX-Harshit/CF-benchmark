from fastapi import APIRouter
from typing import List
from ...schemas.benchmark import BenchmarkScenarioSchema

router = APIRouter()

MOCK_SCENARIOS = [
    {
        "id": "objection_existing_solution_001",
        "category": "existing_solution",
        "name": "Already using competitor",
        "prospect_context": {"role": "VP Sales", "company_size": 200, "industry": "SaaS"},
        "conversation_context": {"stage": "discovery", "pain_points": ["low outbound conversion"]},
        "objection": {"text": "We're already using Salesforce. We don't need another sales tool."},
        "expected_objectives": ["acknowledge_objection", "differentiate_without_attacking_competitor"]
    }
]

@router.get("/scenarios", response_model=List[BenchmarkScenarioSchema])
def get_scenarios():
    return MOCK_SCENARIOS
