from collections.abc import Sequence

from app.core.exceptions import NotFoundException
from app.modules.prompt_blocks.models import PromptBlock
from app.modules.prompt_blocks.repository import PromptBlockRepository


class PromptBlockService:
    def __init__(self, repository: PromptBlockRepository) -> None:
        self.repository = repository

    async def list_prompt_blocks(
        self, *, page: int, limit: int
    ) -> tuple[Sequence[PromptBlock], int]:
        items = await self.repository.get_all(skip=(page - 1) * limit, limit=limit)
        return items, await self.repository.count()

    async def get_prompt_block(self, prompt_block_id: int) -> PromptBlock:
        block = await self.repository.get_by_id(prompt_block_id)
        if block is None:
            raise NotFoundException(f"Блок промпту з id={prompt_block_id} не знайдено")
        return block
