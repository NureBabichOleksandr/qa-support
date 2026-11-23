from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TicketBrief(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    ticket_id: int
    status: str | None
    agent_name: str | None
    organization: str | None
    request_type: str | None


class TicketRead(TicketBrief):
    tags: str | None
    ticket_created_at: datetime | None
    ticket_updated_at: datetime | None
    first_response_time_sec: int | None
    first_response_breached: bool | None
    handling_time: int | None
    longest_agent_gap_sec: int | None
    avg_gap_sec: int | None
    agent_gap_sec: int | None
    agent_gap_breached: bool | None
    longest_customer_gap_sec: int | None
    avg_customer_gap_sec: int | None
    total_agent_replies: int | None
    total_customer_messages: int | None
    refreshed_at: datetime | None


class TicketFilterParams(BaseModel):
    agent_name: str | None = None
    status: str | None = None
    organization: str | None = None


class AgentEvaluatedTicketsResponse(BaseModel):
    agent_name: str
    evaluated_tickets: int
