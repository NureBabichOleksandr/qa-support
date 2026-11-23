from typing import Annotated

from fastapi import APIRouter, Query

from app.core.schemas import Page
from app.modules.evaluations.dependencies import EvaluationServiceDep
from app.modules.evaluations.schemas import (
    EvaluationDetail,
    EvaluationFilterParams,
    EvaluationListItem,
    MaxEvaluationByTopicResponse,
    MaxEvaluationRow,
)

router = APIRouter(prefix="/evaluations", tags=["evaluations"])


@router.get(
    "",
    response_model=Page[EvaluationListItem],
    summary="Список оцінок (фільтри: тема, тікет, агент, результат)",
)
async def list_evaluations(
    service: EvaluationServiceDep,
    filters: Annotated[EvaluationFilterParams, Query()],
    page: Annotated[int, Query(ge=1)] = 1,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
) -> Page[EvaluationListItem]:
    items, total = await service.list_evaluations(filters, page=page, limit=limit)
    return Page[EvaluationListItem](
        items=[EvaluationListItem.model_validate(e) for e in items],
        total=total,
        page=page,
        limit=limit,
    )


@router.get(
    "/max-by-topic",
    response_model=MaxEvaluationByTopicResponse,
    summary="Оцінки з максимальним балом за темою (таблична функція MAX_EVALUATION_BY_TOPIC)",
)
async def max_evaluation_by_topic(
    service: EvaluationServiceDep,
    topic_label: Annotated[str, Query(min_length=1, examples=["Біллінг"])],
) -> MaxEvaluationByTopicResponse:
    rows = await service.max_by_topic(topic_label)
    return MaxEvaluationByTopicResponse(
        topic_label=topic_label, items=[MaxEvaluationRow.model_validate(r) for r in rows]
    )


@router.get(
    "/{qa_evaluation_id}",
    response_model=EvaluationDetail,
    summary="Оцінка з темою, тікетом і блоками промпту",
)
async def get_evaluation(service: EvaluationServiceDep, qa_evaluation_id: int) -> EvaluationDetail:
    return EvaluationDetail.model_validate(await service.get_evaluation(qa_evaluation_id))
