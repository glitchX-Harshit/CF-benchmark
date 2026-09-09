from datetime import datetime
import uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, JSON, Float, ForeignKey, Text
from app.db.base import Base

class Evaluation(Base):
    __tablename__ = "evaluations"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    scenario_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("scenarios.id"))
    seller_response: Mapped[str] = mapped_column(Text)
    overall_score: Mapped[float] = mapped_column(Float)
    response_quality_score: Mapped[float] = mapped_column(Float)
    objection_handling_score: Mapped[float] = mapped_column(Float)
    forward_momentum_score: Mapped[float] = mapped_column(Float)
    evaluation_version: Mapped[str] = mapped_column(String)
    raw_result: Mapped[dict] = mapped_column(JSON)
    strengths: Mapped[list] = mapped_column(JSON)
    weaknesses: Mapped[list] = mapped_column(JSON)
    missed_opportunities: Mapped[list] = mapped_column(JSON)
    recommended_strategy: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

    scores: Mapped[list["DimensionScore"]] = relationship(
        "DimensionScore", back_populates="evaluation", cascade="all, delete-orphan"
    )


class DimensionScore(Base):
    __tablename__ = "dimension_scores"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    evaluation_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("evaluations.id"))
    dimension: Mapped[str] = mapped_column(String)
    score: Mapped[float] = mapped_column(Float)
    reasoning: Mapped[str] = mapped_column(Text)
    evidence: Mapped[list[str]] = mapped_column(JSON, default=list)
    
    evaluation: Mapped[Evaluation] = relationship(back_populates="scores")
