from typing import Annotated

from fastapi import Depends

from app.core.database import SessionDep
from app.modules.prompt_blocks.repository import PromptBlockRepository
from app.modules.prompt_blocks.service import PromptBlockService


async def get_prompt_block_repository(session: SessionDep) -> PromptBlockRepository:
    return PromptBlockRepository(session)


async def get_prompt_block_service(
    repository: Annotated[PromptBlockRepository, Depends(get_prompt_block_repository)],
) -> PromptBlockService:
    return PromptBlockService(repository)


PromptBlockServiceDep = Annotated[PromptBlockService, Depends(get_prompt_block_service)]
