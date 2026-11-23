from typing import Annotated

from fastapi import Depends

from app.core.database import SessionDep
from app.modules.topics.repository import TopicRepository
from app.modules.topics.service import TopicService


async def get_topic_repository(session: SessionDep) -> TopicRepository:
    return TopicRepository(session)


async def get_topic_service(
    repository: Annotated[TopicRepository, Depends(get_topic_repository)],
) -> TopicService:
    return TopicService(repository)


TopicServiceDep = Annotated[TopicService, Depends(get_topic_service)]
