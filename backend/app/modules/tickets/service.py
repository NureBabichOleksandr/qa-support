from collections.abc import Sequence

from app.core.exceptions import NotFoundException
from app.modules.tickets.models import TicketSlaCache
from app.modules.tickets.repository import TicketRepository
from app.modules.tickets.schemas import TicketFilterParams


class TicketService:
    def __init__(self, repository: TicketRepository) -> None:
        self.repository = repository

    async def list_tickets(
        self, filters: TicketFilterParams, *, page: int, limit: int
    ) -> tuple[Sequence[TicketSlaCache], int]:
        return await self.repository.list_filtered(
            agent_name=filters.agent_name,
            status=filters.status,
            organization=filters.organization,
            skip=(page - 1) * limit,
            limit=limit,
        )

    async def get_ticket(self, ticket_id: int) -> TicketSlaCache:
        ticket = await self.repository.get_by_id(ticket_id)
        if ticket is None:
            raise NotFoundException(f"Тікет {ticket_id} не знайдено")
        return ticket

    async def list_agent_names(self) -> Sequence[str]:
        return await self.repository.list_agent_names()

    async def count_evaluated_by_agent(self, agent_name: str) -> int:
        return await self.repository.count_evaluated_by_agent(agent_name)
