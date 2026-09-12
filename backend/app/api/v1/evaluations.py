from fastapi import APIRouter, Depends
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func
from ...models.evaluation import Evaluation
from ...models.scenario import Scenario
from ...core.database import get_db

router = APIRouter()

@router.get("/stats")
def get_dashboard_stats(db: Session = Depends(get_db)):
    eval_count = db.query(Evaluation).count()
    scenario_count = db.query(Scenario).count()
    
    avg_score = db.query(func.avg(Evaluation.final_score)).scalar()
    avg_score = round(avg_score, 1) if avg_score else 0.0

    return {
        "stats": [
            {"label": "Conversations analyzed", "value": str(eval_count), "change": "", "icon": "MessageSquare"},
            {"label": "Average response score", "value": str(avg_score), "change": "", "icon": "TrendingUp"},
            {"label": "Benchmark scenarios", "value": str(scenario_count), "change": "", "icon": "BarChart3"},
            {"label": "Active prospects", "value": "-", "change": "", "icon": "Users"},
        ]
    }

@router.get("/recent")
def get_recent_evaluations(limit: int = 4, db: Session = Depends(get_db)):
    recent = db.query(Evaluation).order_by(Evaluation.created_at.desc()).limit(limit).all()
    
    results = []
    for r in recent:
        results.append({
            "company": r.prospect_role, 
            "objection": r.objection_text[:30] + "..." if len(r.objection_text) > 30 else r.objection_text,
            "time": r.created_at.strftime("%b %d, %H:%M"),
            "score": r.final_score
        })
        
    return results
