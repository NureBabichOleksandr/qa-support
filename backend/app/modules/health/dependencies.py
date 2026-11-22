from app.core.database import SessionDep
from app.modules.health.service import HealthService


async def get_health_service(session: SessionDep) -> HealthService:
    return HealthService(session)
