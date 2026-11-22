from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.dialects.mssql import DATETIME2
from sqlalchemy.orm import Mapped, mapped_column

from app.core.models import Base


class TicketSlaCache(Base):
    """Кеш SLA-метрик тікетів. ticket_id приходить із зовнішньої системи, тому не IDENTITY."""

    __tablename__ = "ticket_sla_cache"

    ticket_id: Mapped[int] = mapped_column(sa.Integer, primary_key=True, autoincrement=False)
    status: Mapped[str | None] = mapped_column(sa.Unicode(20), nullable=True)
    agent_name: Mapped[str | None] = mapped_column(sa.Unicode(50), nullable=True)
    organization: Mapped[str | None] = mapped_column(sa.Unicode(100), nullable=True)
    request_type: Mapped[str | None] = mapped_column(sa.Unicode(50), nullable=True)
    # ЛР2: розширено з NVARCHAR(200) до NVARCHAR(MAX), бо тригер дописує сюди номери оцінок
    tags: Mapped[str | None] = mapped_column(sa.UnicodeText, nullable=True)
    ticket_created_at: Mapped[datetime | None] = mapped_column(DATETIME2, nullable=True)
    ticket_updated_at: Mapped[datetime | None] = mapped_column(DATETIME2, nullable=True)
    first_response_time_sec: Mapped[int | None] = mapped_column(sa.Integer, nullable=True)
    first_response_breached: Mapped[bool | None] = mapped_column(sa.Boolean, nullable=True)
    handling_time: Mapped[int | None] = mapped_column(sa.Integer, nullable=True)
    longest_agent_gap_sec: Mapped[int | None] = mapped_column(sa.Integer, nullable=True)
    avg_gap_sec: Mapped[int | None] = mapped_column(sa.Integer, nullable=True)
    agent_gap_sec: Mapped[int | None] = mapped_column(sa.Integer, nullable=True)
    agent_gap_breached: Mapped[bool | None] = mapped_column(sa.Boolean, nullable=True)
    longest_customer_gap_sec: Mapped[int | None] = mapped_column(sa.Integer, nullable=True)
    avg_customer_gap_sec: Mapped[int | None] = mapped_column(sa.Integer, nullable=True)
    total_agent_replies: Mapped[int | None] = mapped_column(sa.Integer, nullable=True)
    total_customer_messages: Mapped[int | None] = mapped_column(sa.Integer, nullable=True)
    refreshed_at: Mapped[datetime | None] = mapped_column(DATETIME2, nullable=True)
