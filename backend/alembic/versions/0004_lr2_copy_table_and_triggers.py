"""ЛР2, додатки А–В: таблиця qa_evaluation_copy, розширення tags, тригери

Revision ID: 0004
Revises: 0003
Create Date: 2026-11-22

Тексти тригерів перенесено дослівно з sql/01_restore_QA_Support.sql.
"""

from collections.abc import Sequence
from decimal import Decimal

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.mssql import DATETIME2

revision: str = "0004"
down_revision: str | None = "0003"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

SCORE: sa.DECIMAL[Decimal] = sa.DECIMAL(4, 1)


def _execute(sql: str) -> None:
    op.execute(sa.text(sql.replace(":", r"\:")))


# Додаток Б, завдання 1: кожен 3-й змінений рядок копіюється в qa_evaluation_copy
TR_QA_EVALUATION_COPY_SCORE = """
CREATE OR ALTER TRIGGER tr_qa_evaluation_copy_score
ON dbo.qa_evaluation
AFTER UPDATE AS
BEGIN
    IF NOT UPDATE (overall_score)
        RETURN;

    WITH changed_rows AS (
        SELECT ins.qa_evaluation_id, ins.canonical_topic_id, ins.ticket_id, ins.result,
               del.overall_score AS old_score,
               ins.overall_score AS new_score,
               ins.raw_issue_topic,
               ROW_NUMBER() OVER (ORDER BY ins.qa_evaluation_id) AS row_num
        FROM inserted AS ins
        JOIN deleted  AS del ON del.qa_evaluation_id = ins.qa_evaluation_id
        WHERE ISNULL(ins.overall_score, -999) <> ISNULL(del.overall_score, -999)
    )
    INSERT INTO dbo.qa_evaluation_copy (
        qa_evaluation_id, canonical_topic_id, ticket_id,
        result, overall_score_old, overall_score_new, raw_issue_topic, agent_name
    )
    SELECT c.qa_evaluation_id, c.canonical_topic_id, c.ticket_id, c.result,
           c.old_score, c.new_score, c.raw_issue_topic, t.agent_name
    FROM changed_rows AS c
    LEFT JOIN ticket_sla_cache AS t ON t.ticket_id = c.ticket_id
    WHERE c.row_num % 3 = 0;
END
"""

# Додаток В, завдання 4: номери нових оцінок дописуються в ticket_sla_cache.tags
TR_QA_EVALUATION_ADD_TO_TICKET = """
CREATE OR ALTER TRIGGER tr_qa_evaluation_add_to_ticket
ON dbo.qa_evaluation
AFTER INSERT AS
BEGIN
    WITH inserted_rows AS (
        SELECT ticket_id,
               STRING_AGG(CAST(qa_evaluation_id AS NVARCHAR(20)), N', ') AS eval_ids
        FROM inserted
        WHERE ticket_id IS NOT NULL
        GROUP BY ticket_id
    )
    UPDATE t
    SET tags              = ISNULL(t.tags + N'; ', N'') + N'Оцінка: ' + r.eval_ids,
        ticket_updated_at = SYSDATETIME()
    FROM dbo.ticket_sla_cache AS t
    JOIN inserted_rows        AS r ON r.ticket_id = t.ticket_id;
END
"""


def upgrade() -> None:
    # Додаток А, завдання 1
    op.create_table(
        "qa_evaluation_copy",
        sa.Column("id", sa.Integer, sa.Identity(start=1, increment=1), nullable=False),
        sa.Column("qa_evaluation_id", sa.Integer, nullable=False),
        sa.Column("canonical_topic_id", sa.Integer, nullable=True),
        sa.Column("ticket_id", sa.Integer, nullable=True),
        sa.Column("result", sa.Unicode(20), nullable=True),
        sa.Column("overall_score_old", SCORE, nullable=True),
        sa.Column("overall_score_new", SCORE, nullable=True),
        sa.Column("raw_issue_topic", sa.Unicode(200), nullable=True),
        sa.Column("agent_name", sa.Unicode(50), nullable=True),
        sa.Column("copied_at", DATETIME2, server_default=sa.text("SYSDATETIME()"), nullable=False),
        sa.PrimaryKeyConstraint("id", name="pk_qa_evaluation_copy"),
    )

    # Додаток В: tags NVARCHAR(200) -> NVARCHAR(MAX)
    op.alter_column(
        "ticket_sla_cache",
        "tags",
        type_=sa.UnicodeText,
        existing_type=sa.Unicode(200),
        existing_nullable=True,
    )

    _execute(TR_QA_EVALUATION_COPY_SCORE)
    _execute(TR_QA_EVALUATION_ADD_TO_TICKET)


def downgrade() -> None:
    _execute("DROP TRIGGER IF EXISTS dbo.tr_qa_evaluation_add_to_ticket;")
    _execute("DROP TRIGGER IF EXISTS dbo.tr_qa_evaluation_copy_score;")
    # УВАГА: якщо якийсь tags довший за 200 символів, цей крок впаде з помилкою обрізання
    op.alter_column(
        "ticket_sla_cache",
        "tags",
        type_=sa.Unicode(200),
        existing_type=sa.UnicodeText,
        existing_nullable=True,
    )
    op.drop_table("qa_evaluation_copy")
