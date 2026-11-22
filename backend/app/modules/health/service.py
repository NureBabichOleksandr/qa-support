import logging

from sqlalchemy import text
from sqlalchemy.exc import DBAPIError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ServiceUnavailableException

logger = logging.getLogger("qa-support.health")


class HealthService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def check(self) -> str:
        try:
            result = await self.session.execute(text("SELECT DB_NAME()"))
        except DBAPIError as exc:
            logger.warning("Database health check failed: %s", exc.__class__.__name__)
            raise ServiceUnavailableException("Database is unavailable") from exc
        return str(result.scalar_one())
