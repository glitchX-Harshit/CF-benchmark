from sqlalchemy import Column, String, Integer, Float, JSON, DateTime
from ..core.database import Base
from datetime import datetime
import uuid

def generate_uuid():
    return str(uuid.uuid4())

class Evaluation(Base):
    __tablename__ = "evaluations"

    id = Column(String, primary_key=True, index=True, default=generate_uuid)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Store minimal info for the dashboard
    prospect_role = Column(String)
    objection_text = Column(String)
    seller_response = Column(String)
    
    # Scores
    final_score = Column(Integer)
    response_quality = Column(Integer)
    strategic_opportunity = Column(Integer)
    direction_score = Column(Integer)
    
    # Full JSON report for reference
    report_data = Column(JSON)
