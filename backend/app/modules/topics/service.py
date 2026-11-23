from collections.abc import Sequence

from app.core.exceptions import NotFoundException
from app.modules.topics.exceptions import TopicHasNoOrganizationsError, TopicNotFoundError
from app.modules.topics.models import CanonicalTopic
from app.modules.topics.repository import TopicRepository
from app.modules.topics.schemas import TopicFilterParams

# Коди повернення dbo.SET_TOP_ORGANIZATION_FOR_TOPIC
RC_OK, RC_TOPIC_NOT_FOUND, RC_NO_ORGANIZATIONS = 0, 1, 2


class TopicService:
    def __init__(self, repository: TopicRepository) -> None:
        self.repository = repository

    async def list_topics(
        self, filters: TopicFilterParams, *, page: int, limit: int
    ) -> tuple[Sequence[CanonicalTopic], int]:
        return await self.repository.list_filtered(
            search=filters.search,
            is_active=filters.is_active,
            skip=(page - 1) * limit,
            limit=limit,
        )

    async def get_topic(self, canonical_topic_id: int) -> CanonicalTopic:
        topic = await self.repository.get_by_id(canonical_topic_id)
        if topic is None:
            raise NotFoundException(f"Тему з id={canonical_topic_id} не знайдено")
        return topic

    async def top_topics_by_agent(self, agent_name: str) -> Sequence[str]:
        return await self.repository.top_topics_by_agent(agent_name)

    async def set_priority(self, topic_label: str, priority_percent: int) -> CanonicalTopic:
        # Порожню назву відхиляє сама процедура (THROW 50001) -> обробник DBAPIError -> 400
        await self.repository.set_priority(topic_label, priority_percent)
        topic = await self.repository.get_by_label(topic_label)
        if topic is None:
            raise TopicNotFoundError(topic_label)
        return topic

    async def set_top_organization(self, topic_label: str) -> CanonicalTopic:
        rc = await self.repository.set_top_organization(topic_label)
        if rc == RC_TOPIC_NOT_FOUND:
            raise TopicNotFoundError(topic_label)
        if rc == RC_NO_ORGANIZATIONS:
            raise TopicHasNoOrganizationsError(topic_label)
        topic = await self.repository.get_by_label(topic_label)
        if topic is None:
            raise TopicNotFoundError(topic_label)
        return topic
