from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session
from ...schemas.benchmark import BenchmarkScenarioSchema
from ...models.scenario import Scenario
from ...core.database import get_db

router = APIRouter()

MOCK_SCENARIOS = [
    {
        "id": "objection_existing_solution_001",
        "category": "existing_solution",
        "name": "Already using Salesforce",
        "prospect_context": {"role": "VP Sales", "company_size": 200, "industry": "SaaS"},
        "conversation_context": {"stage": "discovery", "pain_points": ["low outbound conversion"]},
        "objection": {"text": "We're already using Salesforce. We don't need another sales tool."},
        "expected_objectives": ["acknowledge_objection", "differentiate_without_attacking_competitor"]
    },
    {
        "id": "objection_brush_off_001",
        "category": "brush_off",
        "name": "Send me an email",
        "prospect_context": {"role": "Chief Marketing Officer", "company_size": 500, "industry": "Retail"},
        "conversation_context": {"stage": "opening", "pain_points": ["high customer acquisition cost"]},
        "objection": {"text": "I'm stepping into a meeting right now. Just send me an email with some info and I'll take a look."},
        "expected_objectives": ["secure_time", "avoid_premature_pitch", "create_curiosity"]
    },
    {
        "id": "objection_budget_001",
        "category": "budget",
        "name": "No budget right now",
        "prospect_context": {"role": "Director of IT", "company_size": 1500, "industry": "Manufacturing"},
        "conversation_context": {"stage": "discovery", "pain_points": ["legacy systems", "high maintenance costs"]},
        "objection": {"text": "We just finalized our budget for the year and everything is locked. We have no budget for new software."},
        "expected_objectives": ["reduce_friction", "shift_to_timeline_discovery", "validate_prospect"]
    },
    {
        "id": "objection_timing_001",
        "category": "timing",
        "name": "Too busy right now",
        "prospect_context": {"role": "Founder", "company_size": 50, "industry": "Fintech"},
        "conversation_context": {"stage": "opening", "pain_points": ["scaling operations", "compliance tracking"]},
        "objection": {"text": "Look, we're extremely busy with a product launch this quarter. Call me back in 6 months."},
        "expected_objectives": ["respect_timing", "discover_priority", "leave_door_open"]
    },
    {
        "id": "objection_price_indian_001",
        "category": "price",
        "name": "Local Price / Budget (India)",
        "prospect_context": {"role": "Owner/Founder", "company_size": 30, "industry": "Manufacturing"},
        "conversation_context": {"stage": "commercial", "pain_points": ["high cost", "price sensitivity"]},
        "objection": {"text": "Sir, this is way too expensive for us. We can get this done much cheaper locally or just use Excel."},
        "expected_objectives": ["validate_prospect", "shift_to_value", "differentiate_on_quality"]
    },
    {
        "id": "objection_trust_indian_001",
        "category": "trust",
        "name": "Family Vendor (India)",
        "prospect_context": {"role": "Managing Director", "company_size": 100, "industry": "Wholesale"},
        "conversation_context": {"stage": "discovery", "pain_points": ["vendor complacency", "slow delivery"]},
        "objection": {"text": "Hum pichle 10 saal se apne ek family vendor ke saath kaam kar rahe hain. I don't want to break that relationship."},
        "expected_objectives": ["respect_existing_solution", "position_complementary", "create_gap_opening"]
    },
    {
        "id": "objection_authority_indian_001",
        "category": "authority",
        "name": "Partner/CA Decision (India)",
        "prospect_context": {"role": "Partner", "company_size": 15, "industry": "Services"},
        "conversation_context": {"stage": "closing", "pain_points": ["decision bottlenecks"]},
        "objection": {"text": "I can't take this decision alone. I need to discuss this with my partner and my CA first."},
        "expected_objectives": ["acknowledge_authority", "secure_next_steps_with_all_parties"]
    }
]

@router.get("/scenarios", response_model=List[BenchmarkScenarioSchema])
def get_scenarios(db: Session = Depends(get_db)):
    scenarios = db.query(Scenario).all()
    
    # Auto-seed missing mock scenarios into the DB
    existing_ids = {s.id for s in scenarios}
    seeded_new = False
    for mock in MOCK_SCENARIOS:
        if mock["id"] not in existing_ids:
            db_scenario = Scenario(
                id=mock["id"],
                category=mock["category"],
                name=mock["name"],
                prospect_context=mock["prospect_context"],
                conversation_context=mock["conversation_context"],
                objection=mock["objection"],
                expected_objectives=mock["expected_objectives"]
            )
            db.add(db_scenario)
            seeded_new = True
            
    if seeded_new:
        db.commit()
        scenarios = db.query(Scenario).all()
        
    return scenarios

@router.post("/scenarios", response_model=BenchmarkScenarioSchema)
def create_scenario(scenario: BenchmarkScenarioSchema, db: Session = Depends(get_db)):
    db_scenario = Scenario(
        id=scenario.id,
        category=scenario.category,
        name=scenario.name,
        prospect_context=scenario.prospect_context,
        conversation_context=scenario.conversation_context,
        objection=scenario.objection,
        expected_objectives=scenario.expected_objectives
    )
    db.add(db_scenario)
    db.commit()
    db.refresh(db_scenario)
    return db_scenario
