from typing import Annotated

from fastapi import APIRouter, Query

from app.core.schemas import Page
from app.modules.prompt_blocks.dependencies import PromptBlockServiceDep
from app.modules.prompt_blocks.schemas import PromptBlockRead

router = APIRouter(prefix="/prompt-blocks", tags=["prompt-blocks"])


@router.get("", response_model=Page[PromptBlockRead], summary="Список блоків промпту")
async def list_prompt_blocks(
    service: PromptBlockServiceDep,
    page: Annotated[int, Query(ge=1)] = 1,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
) -> Page[PromptBlockRead]:
    items, total = await service.list_prompt_blocks(page=page, limit=limit)
    return Page[PromptBlockRead](
        items=[PromptBlockRead.model_validate(b) for b in items],
        total=total,
        page=page,
        limit=limit,
    )


@router.get("/{prompt_block_id}", response_model=PromptBlockRead, summary="Блок промпту за id")
async def get_prompt_block(service: PromptBlockServiceDep, prompt_block_id: int) -> PromptBlockRead:
    return PromptBlockRead.model_validate(await service.get_prompt_block(prompt_block_id))
