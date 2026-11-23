from typing import Annotated, Any

from fastapi import APIRouter, Query

from app.core.schemas import Page
from app.modules.topics.dependencies import TopicServiceDep
from app.modules.topics.schemas import (
    TopicFilterParams,
    TopicPriorityRequest,
    TopicRead,
    TopOrganizationRequest,
    TopTopicsByAgentResponse,
)

router = APIRouter(prefix="/topics", tags=["topics"])

DB_ERROR_RESPONSE: dict[int | str, dict[str, Any]] = {
    400: {
        "description": "Користувацький виняток з процедури БД (THROW 5xxxx)",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Параметр @topic_label є обов'язковим.",
                    "source": "database",
                    "error_number": 50001,
                }
            }
        },
    }
}


@router.get("", response_model=Page[TopicRead], summary="Список тем")
async def list_topics(
    service: TopicServiceDep,
    filters: Annotated[TopicFilterParams, Query()],
    page: Annotated[int, Query(ge=1)] = 1,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
) -> Page[TopicRead]:
    items, total = await service.list_topics(filters, page=page, limit=limit)
    return Page[TopicRead](
        items=[TopicRead.model_validate(t) for t in items], total=total, page=page, limit=limit
    )


@router.get(
    "/top-by-agent",
    response_model=TopTopicsByAgentResponse,
    summary="Найчастіші теми агента (таблична функція TOP_TOPIC_BY_AGENT_NAME)",
)
async def top_topics_by_agent(
    service: TopicServiceDep,
    agent_name: Annotated[str, Query(min_length=1, examples=["Ковальчук"])],
) -> TopTopicsByAgentResponse:
    labels = await service.top_topics_by_agent(agent_name)
    return TopTopicsByAgentResponse(agent_name=agent_name, topic_labels=list(labels))


@router.post(
    "/priority",
    response_model=TopicRead,
    summary="Встановити пріоритет теми (процедура SET_TOPIC_PRIORITY)",
    responses=DB_ERROR_RESPONSE,
)
async def set_topic_priority(service: TopicServiceDep, data: TopicPriorityRequest) -> TopicRead:
    topic = await service.set_priority(data.topic_label, data.priority_percent)
    return TopicRead.model_validate(topic)


@router.post(
    "/top-organization",
    response_model=TopicRead,
    summary="Записати топ-організацію теми (процедура SET_TOP_ORGANIZATION_FOR_TOPIC)",
)
async def set_top_organization(service: TopicServiceDep, data: TopOrganizationRequest) -> TopicRead:
    topic = await service.set_top_organization(data.topic_label)
    return TopicRead.model_validate(topic)


@router.get("/{canonical_topic_id}", response_model=TopicRead, summary="Тема за id")
async def get_topic(service: TopicServiceDep, canonical_topic_id: int) -> TopicRead:
    return TopicRead.model_validate(await service.get_topic(canonical_topic_id))
