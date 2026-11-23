from collections.abc import Sequence
from typing import Any

from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from app.core.repositories import BaseRepository
from app.modules.evaluations.models import QaEvaluation
from app.modules.tickets.models import TicketSlaCache

MAX_EVALUATION_BY_TOPIC = text(
    """
    SELECT qa_evaluation_id, ticket_id, overall_score, result, created_at, info
    FROM dbo.MAX_EVALUATION_BY_TOPIC(:topic_label)
    """
)


class EvaluationRepository(BaseRepository[QaEvaluation]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(QaEvaluation, session)

    async def list_filtered(
        self,
        *,
        canonical_topic_id: int | None,
        ticket_id: int | None,
        agent_name: str | None,
        result: str | None,
        skip: int,
        limit: int,
    ) -> tuple[Sequence[QaEvaluation], int]:
        stmt = select(QaEvaluation).order_by(QaEvaluation.qa_evaluation_id)
        if canonical_topic_id is not None:
            stmt = stmt.where(QaEvaluation.canonical_topic_id == canonical_topic_id)
        if ticket_id is not None:
            stmt = stmt.where(QaEvaluation.ticket_id == ticket_id)
        if agent_name:
            stmt = stmt.join(QaEvaluation.ticket).where(TicketSlaCache.agent_name == agent_name)
        if result:
            stmt = stmt.where(QaEvaluation.result == result)
        return await self.paginate(
            stmt,
            skip=skip,
            limit=limit,
            options=(joinedload(QaEvaluation.topic), joinedload(QaEvaluation.ticket)),
        )

    async def get_detail(self, qa_evaluation_id: int) -> QaEvaluation | None:
        stmt = (
            select(QaEvaluation)
            .where(QaEvaluation.qa_evaluation_id == qa_evaluation_id)
            .options(
                joinedload(QaEvaluation.topic),
                joinedload(QaEvaluation.ticket),
                selectinload(QaEvaluation.prompt_blocks),
            )
        )
        res = await self.session.execute(stmt)
        return res.scalars().first()

    async def max_by_topic(self, topic_label: str) -> list[dict[str, Any]]:
        res = await self.session.execute(MAX_EVALUATION_BY_TOPIC, {"topic_label": topic_label})
        return [dict(row) for row in res.mappings().all()]
