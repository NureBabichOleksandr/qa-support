"""ЛР1, додаток А: таблиці БД QA_Support

Revision ID: 0001
Revises:
Create Date: 2026-11-22
"""

from collections.abc import Sequence
from decimal import Decimal

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.mssql import DATETIME2

revision: str = "0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

NOW = sa.text("SYSDATETIME()")
SCORE: sa.DECIMAL[Decimal] = sa.DECIMAL(4, 1)


def upgrade() -> None:
    op.create_table(
        "canonical_topics",
        sa.Column(
            "canonical_topic_id", sa.Integer, sa.Identity(start=1, increment=1), nullable=False
        ),
        sa.Column("topic_id", sa.Unicode(50), nullable=False),
        sa.Column("topic_label", sa.Unicode(100), nullable=False),
        sa.Column("meaning", sa.Unicode(500), nullable=True),
        sa.Column("is_active", sa.Boolean, server_default=sa.text("1"), nullable=False),
        sa.Column("created_at", DATETIME2, server_default=NOW, nullable=False),
        sa.Column("updated_at", DATETIME2, nullable=True),
        sa.Column("synonyms", sa.Unicode(500), nullable=True),
        sa.Column("client_aliases", sa.Unicode(500), nullable=True),
        sa.Column("related_terms", sa.Unicode(500), nullable=True),
        sa.Column("embedding", sa.LargeBinary, nullable=True),
        sa.PrimaryKeyConstraint("canonical_topic_id", name="pk_canonical_topics"),
        sa.UniqueConstraint("topic_id", name="uq_canonical_topics_topic_id"),
    )

    op.create_table(
        "prompt_block",
        sa.Column("prompt_block_id", sa.Integer, sa.Identity(start=1, increment=1), nullable=False),
        sa.Column("text", sa.UnicodeText, nullable=True),
        sa.Column("version", sa.Unicode(20), nullable=True),
        sa.Column("added_by", sa.Unicode(50), nullable=True),
        sa.Column("created_at", DATETIME2, server_default=NOW, nullable=False),
        sa.PrimaryKeyConstraint("prompt_block_id", name="pk_prompt_block"),
    )

    op.create_table(
        "ticket_sla_cache",
        sa.Column("ticket_id", sa.Integer, autoincrement=False, nullable=False),
        sa.Column("status", sa.Unicode(20), nullable=True),
        sa.Column("agent_name", sa.Unicode(50), nullable=True),
        sa.Column("organization", sa.Unicode(100), nullable=True),
        sa.Column("request_type", sa.Unicode(50), nullable=True),
        sa.Column("tags", sa.Unicode(200), nullable=True),  # NVARCHAR(MAX) з ЛР2, див. 0004
        sa.Column("ticket_created_at", DATETIME2, nullable=True),
        sa.Column("ticket_updated_at", DATETIME2, nullable=True),
        sa.Column("first_response_time_sec", sa.Integer, nullable=True),
        sa.Column("first_response_breached", sa.Boolean, nullable=True),
        sa.Column("handling_time", sa.Integer, nullable=True),
        sa.Column("longest_agent_gap_sec", sa.Integer, nullable=True),
        sa.Column("avg_gap_sec", sa.Integer, nullable=True),
        sa.Column("agent_gap_sec", sa.Integer, nullable=True),
        sa.Column("agent_gap_breached", sa.Boolean, nullable=True),
        sa.Column("longest_customer_gap_sec", sa.Integer, nullable=True),
        sa.Column("avg_customer_gap_sec", sa.Integer, nullable=True),
        sa.Column("total_agent_replies", sa.Integer, nullable=True),
        sa.Column("total_customer_messages", sa.Integer, nullable=True),
        sa.Column("refreshed_at", DATETIME2, nullable=True),
        sa.PrimaryKeyConstraint("ticket_id", name="pk_ticket_sla_cache"),
    )

    op.create_table(
        "qa_evaluation",
        sa.Column(
            "qa_evaluation_id", sa.Integer, sa.Identity(start=1, increment=1), nullable=False
        ),
        sa.Column("canonical_topic_id", sa.Integer, nullable=True),
        sa.Column("ticket_id", sa.Integer, nullable=True),
        sa.Column("result", sa.Unicode(20), nullable=True),
        sa.Column("overall_score", SCORE, nullable=True),
        sa.Column("kb_source_title", sa.Unicode(200), nullable=True),
        sa.Column("kb_source_url", sa.Unicode(400), nullable=True),
        sa.Column("correct_points", sa.UnicodeText, nullable=True),
        sa.Column("missing_points", sa.UnicodeText, nullable=True),
        sa.Column("incorrect_points", sa.UnicodeText, nullable=True),
        sa.Column("communication_issues", sa.UnicodeText, nullable=True),
        sa.Column("qa_comment", sa.UnicodeText, nullable=True),
        sa.Column("recommendation", sa.UnicodeText, nullable=True),
        sa.Column("raw_issue_topic", sa.Unicode(200), nullable=True),
        sa.Column("llm_model", sa.Unicode(50), nullable=True),
        sa.Column("created_at", DATETIME2, server_default=NOW, nullable=False),
        sa.Column("updated_at", DATETIME2, nullable=True),
        sa.Column("organization_name", sa.Unicode(100), nullable=True),
        sa.Column("topic_confidence", sa.DECIMAL(4, 3), nullable=True),
        sa.Column("technical_accuracy_score", SCORE, nullable=True),
        sa.Column("troubleshooting_approach_score", SCORE, nullable=True),
        sa.Column("completeness_score", SCORE, nullable=True),
        sa.Column("case_ownership_score", SCORE, nullable=True),
        sa.Column("technical_quality_score", SCORE, nullable=True),
        sa.Column("communication_quality_score", SCORE, nullable=True),
        sa.PrimaryKeyConstraint("qa_evaluation_id", name="pk_qa_evaluation"),
        sa.ForeignKeyConstraint(
            ["canonical_topic_id"],
            ["canonical_topics.canonical_topic_id"],
            name="fk_qa_eval_topic",
        ),
        sa.ForeignKeyConstraint(
            ["ticket_id"], ["ticket_sla_cache.ticket_id"], name="fk_qa_eval_ticket"
        ),
    )

    op.create_table(
        "qa_evaluation_prompt_block",
        sa.Column(
            "qa_evaluation_prompt_block_id",
            sa.Integer,
            sa.Identity(start=1, increment=1),
            nullable=False,
        ),
        sa.Column("prompt_block_id", sa.Integer, nullable=False),
        sa.Column("qa_evaluation_id", sa.Integer, nullable=False),
        sa.PrimaryKeyConstraint("qa_evaluation_prompt_block_id", name="pk_qa_eval_pb"),
        sa.ForeignKeyConstraint(
            ["prompt_block_id"], ["prompt_block.prompt_block_id"], name="fk_qa_eval_pb_block"
        ),
        sa.ForeignKeyConstraint(
            ["qa_evaluation_id"], ["qa_evaluation.qa_evaluation_id"], name="fk_qa_eval_pb_eval"
        ),
    )


def downgrade() -> None:
    op.drop_table("qa_evaluation_prompt_block")
    op.drop_table("qa_evaluation")
    op.drop_table("ticket_sla_cache")
    op.drop_table("prompt_block")
    op.drop_table("canonical_topics")
