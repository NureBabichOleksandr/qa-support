from typing import Annotated

from fastapi import Depends

from app.core.database import SessionDep
from app.modules.tickets.repository import TicketRepository
from app.modules.tickets.service import TicketService


async def get_ticket_repository(session: SessionDep) -> TicketRepository:
    return TicketRepository(session)


async def get_ticket_service(
    repository: Annotated[TicketRepository, Depends(get_ticket_repository)],
) -> TicketService:
    return TicketService(repository)


TicketServiceDep = Annotated[TicketService, Depends(get_ticket_service)]
