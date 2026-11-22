from typing import Annotated

from fastapi import APIRouter, Depends

from app.modules.health.dependencies import get_health_service
from app.modules.health.schemas import HealthResponse
from app.modules.health.service import HealthService

router = APIRouter(prefix="/health", tags=["health"])


@router.get("", response_model=HealthResponse, summary="Перевірка API та з'єднання з БД")
async def health(
    service: Annotated[HealthService, Depends(get_health_service)],
) -> HealthResponse:
    database = await service.check()
    return HealthResponse(status="ok", database=database)
