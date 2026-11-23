"""Скалярна функція dbo.req_count_by_agnet_NAME

Revision ID: 0005
Revises: 0004
Create Date: 2026-11-22

Кількість різних тікетів агента, які мають хоча б одну оцінку.
Назва (з «agnet») збережена як у попередніх ЛР.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0005"
down_revision: str | None = "0004"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

REQ_COUNT_BY_AGENT_NAME = """
CREATE OR ALTER FUNCTION dbo.req_count_by_agnet_NAME
(@agent_name NVARCHAR(50))
RETURNS int
AS
BEGIN
RETURN (
SELECT COUNT(DISTINCT qa_evaluation.ticket_id)
FROM qa_evaluation
JOIN ticket_sla_cache ON qa_evaluation.ticket_id = ticket_sla_cache.ticket_id
WHERE ticket_sla_cache.agent_name = @agent_name
);
END
"""


def upgrade() -> None:
    op.execute(sa.text(REQ_COUNT_BY_AGENT_NAME))


def downgrade() -> None:
    op.execute(sa.text("DROP FUNCTION IF EXISTS dbo.req_count_by_agnet_NAME;"))
