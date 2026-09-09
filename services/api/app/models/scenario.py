from datetime import datetime
import uuid
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime, JSON, Enum, Text
from app.db.base import Base
import enum

class SalesStage(str, enum.Enum):
    COLD_CALL = "cold_call"
    DISCOVERY = "discovery"
    QUALIFICATION = "qualification"
    DEMO = "demo"
    TECHNICAL_VALIDATION = "technical_validation"
    DEMO_FOLLOWUP = "demo_followup"
    PROPOSAL = "proposal"
    NEGOTIATION = "negotiation"
    CLOSING = "closing"

class Scenario(Base):
    __tablename__ = "scenarios"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(Text)
    industry: Mapped[str] = mapped_column(String)
    sales_stage: Mapped[SalesStage] = mapped_column(Enum(SalesStage))
    prospect_role: Mapped[str] = mapped_column(String)
    company_context: Mapped[dict] = mapped_column(JSON)
    prospect_context: Mapped[dict] = mapped_column(JSON)
    objection: Mapped[str] = mapped_column(Text)
    hidden_concern: Mapped[list] = mapped_column(JSON)
    desired_outcome: Mapped[list] = mapped_column(JSON)
    expected_strategy: Mapped[list] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
