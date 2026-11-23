from sqlalchemy.ext.asyncio import AsyncSession

from app.core.repositories import BaseRepository
from app.modules.prompt_blocks.models import PromptBlock


class PromptBlockRepository(BaseRepository[PromptBlock]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(PromptBlock, session)
