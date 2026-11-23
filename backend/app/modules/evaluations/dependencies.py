from typing import Annotated

from fastapi import Depends

from app.core.database import SessionDep
from app.modules.evaluations.repository import EvaluationRepository
from app.modules.evaluations.service import EvaluationService


async def get_evaluation_repository(session: SessionDep) -> EvaluationRepository:
    return EvaluationRepository(session)


async def get_evaluation_service(
    repository: Annotated[EvaluationRepository, Depends(get_evaluation_repository)],
) -> EvaluationService:
    return EvaluationService(repository)


EvaluationServiceDep = Annotated[EvaluationService, Depends(get_evaluation_service)]
