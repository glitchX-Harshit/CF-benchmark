from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.evaluation import Evaluation, DimensionScore
from app.schemas.analytics import AnalyticsOverview, AnalyticsDimensions

class AnalyticsService:
    async def get_overview(self, db: AsyncSession) -> AnalyticsOverview:
        result = await db.execute(
            select(
                func.count(Evaluation.id),
                func.avg(Evaluation.overall_score),
                func.avg(Evaluation.response_quality_score),
                func.avg(Evaluation.objection_handling_score),
                func.avg(Evaluation.forward_momentum_score)
            )
        )
        row = result.first()
        return AnalyticsOverview(
            total_evaluations=row[0] or 0,
            average_overall_score=row[1] or 0.0,
            average_response_quality=row[2] or 0.0,
            average_objection_handling=row[3] or 0.0,
            average_forward_momentum=row[4] or 0.0
        )

    async def get_dimensions(self, db: AsyncSession) -> AnalyticsDimensions:
        result = await db.execute(
            select(DimensionScore.dimension, func.avg(DimensionScore.score))
            .group_by(DimensionScore.dimension)
        )
        rows = result.all()
        return AnalyticsDimensions(
            dimension_averages={row[0]: row[1] for row in rows}
        )

analytics_service = AnalyticsService()
