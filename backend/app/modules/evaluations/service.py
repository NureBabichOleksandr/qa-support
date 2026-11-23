from collections.abc import Sequence
from typing import Any

from app.core.exceptions import NotFoundException
from app.modules.evaluations.models import QaEvaluation
from app.modules.evaluations.repository import EvaluationRepository
from app.modules.evaluations.schemas import EvaluationFilterParams


class EvaluationService:
    def __init__(self, repository: EvaluationRepository) -> None:
        self.repository = repository

    async def list_evaluations(
        self, filters: EvaluationFilterParams, *, page: int, limit: int
    ) -> tuple[Sequence[QaEvaluation], int]:
        return await self.repository.list_filtered(
            canonical_topic_id=filters.canonical_topic_id,
            ticket_id=filters.ticket_id,
            agent_name=filters.agent_name,
            result=filters.result,
            skip=(page - 1) * limit,
            limit=limit,
        )

    async def get_evaluation(self, qa_evaluation_id: int) -> QaEvaluation:
        evaluation = await self.repository.get_detail(qa_evaluation_id)
        if evaluation is None:
            raise NotFoundException(f"Оцінку з id={qa_evaluation_id} не знайдено")
        return evaluation

    async def max_by_topic(self, topic_label: str) -> list[dict[str, Any]]:
        return await self.repository.max_by_topic(topic_label)
