from typing import Annotated

from fastapi import APIRouter, Path, Query

from app.core.schemas import Page
from app.modules.tickets.dependencies import TicketServiceDep
from app.modules.tickets.schemas import (
    AgentEvaluatedTicketsResponse,
    TicketFilterParams,
    TicketRead,
)

router = APIRouter(prefix="/tickets", tags=["tickets"])


@router.get("", response_model=Page[TicketRead], summary="Список тікетів")
async def list_tickets(
    service: TicketServiceDep,
    filters: Annotated[TicketFilterParams, Query()],
    page: Annotated[int, Query(ge=1)] = 1,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
) -> Page[TicketRead]:
    items, total = await service.list_tickets(filters, page=page, limit=limit)
    return Page[TicketRead](
        items=[TicketRead.model_validate(t) for t in items], total=total, page=page, limit=limit
    )


@router.get("/agents", response_model=list[str], summary="Імена агентів")
async def list_agents(service: TicketServiceDep) -> list[str]:
    return list(await service.list_agent_names())


@router.get(
    "/agents/{agent_name}/evaluated-tickets-count",
    response_model=AgentEvaluatedTicketsResponse,
    summary="Кількість оцінених тікетів агента",
)
async def count_evaluated_tickets(
    service: TicketServiceDep,
    agent_name: Annotated[str, Path(min_length=1, examples=["Ковальчук"])],
) -> AgentEvaluatedTicketsResponse:
    count = await service.count_evaluated_by_agent(agent_name)
    return AgentEvaluatedTicketsResponse(agent_name=agent_name, evaluated_tickets=count)


@router.get("/{ticket_id}", response_model=TicketRead, summary="Тікет за номером")
async def get_ticket(service: TicketServiceDep, ticket_id: int) -> TicketRead:
    return TicketRead.model_validate(await service.get_ticket(ticket_id))
