from sqlalchemy import Column, String, JSON
from ..core.database import Base
import uuid

def generate_uuid():
    return str(uuid.uuid4())

class Scenario(Base):
    __tablename__ = "scenarios"

    id = Column(String, primary_key=True, index=True, default=generate_uuid)
    category = Column(String, index=True)
    name = Column(String, index=True)
    
    # Store these as JSON columns so they easily map to our Pydantic schemas
    prospect_context = Column(JSON, default=dict)
    conversation_context = Column(JSON, default=dict)
    objection = Column(JSON, default=dict)
    expected_objectives = Column(JSON, default=list)
