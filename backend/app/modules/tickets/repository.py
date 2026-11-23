from collections.abc import Sequence

from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.repositories import BaseRepository
from app.modules.tickets.models import TicketSlaCache

# FUNCTION
REQ_COUNT_BY_AGENT_NAME = text("SELECT dbo.req_count_by_agnet_NAME(:agent_name)")


class TicketRepository(BaseRepository[TicketSlaCache]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(TicketSlaCache, session)

    async def list_filtered(
        self,
        *,
        agent_name: str | None,
        status: str | None,
        organization: str | None,
        skip: int,
        limit: int,
    ) -> tuple[Sequence[TicketSlaCache], int]:
        stmt = select(TicketSlaCache).order_by(TicketSlaCache.ticket_id)
        if agent_name:
            stmt = stmt.where(TicketSlaCache.agent_name == agent_name)
        if status:
            stmt = stmt.where(TicketSlaCache.status == status)
        if organization:
            stmt = stmt.where(TicketSlaCache.organization == organization)
        return await self.paginate(stmt, skip=skip, limit=limit)

    async def list_agent_names(self) -> Sequence[str]:
        stmt = (
            select(TicketSlaCache.agent_name)
            .where(TicketSlaCache.agent_name.is_not(None))
            .distinct()
            .order_by(TicketSlaCache.agent_name)
        )
        result = await self.session.execute(stmt)
        return [name for name in result.scalars().all() if name is not None]

    async def count_evaluated_by_agent(self, agent_name: str) -> int:
        result = await self.session.execute(REQ_COUNT_BY_AGENT_NAME, {"agent_name": agent_name})
        return int(result.scalar_one())
