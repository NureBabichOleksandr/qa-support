from datetime import datetime
from decimal import Decimal

import sqlalchemy as sa
from sqlalchemy.dialects.mssql import DATETIME2
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.models import Base
from app.modules.prompt_blocks.models import PromptBlock
from app.modules.tickets.models import TicketSlaCache
from app.modules.topics.models import CanonicalTopic

Score: sa.DECIMAL[Decimal] = sa.DECIMAL(4, 1)


class QaEvaluation(Base):
    __tablename__ = "qa_evaluation"
    # На таблиці є AFTER INSERT/UPDATE тригери (ЛР2): OUTPUT inserted з ними несумісний
    __table_args__ = ({"implicit_returning": False},)

    qa_evaluation_id: Mapped[int] = mapped_column(
        sa.Integer, sa.Identity(start=1, increment=1), primary_key=True
    )
    canonical_topic_id: Mapped[int | None] = mapped_column(
        sa.Integer,
        sa.ForeignKey("canonical_topics.canonical_topic_id", name="fk_qa_eval_topic"),
        nullable=True,
    )
    ticket_id: Mapped[int | None] = mapped_column(
        sa.Integer,
        sa.ForeignKey("ticket_sla_cache.ticket_id", name="fk_qa_eval_ticket"),
        nullable=True,
    )
    result: Mapped[str | None] = mapped_column(sa.Unicode(20), nullable=True)
    overall_score: Mapped[Decimal | None] = mapped_column(Score, nullable=True)
    kb_source_title: Mapped[str | None] = mapped_column(sa.Unicode(200), nullable=True)
    kb_source_url: Mapped[str | None] = mapped_column(sa.Unicode(400), nullable=True)
    correct_points: Mapped[str | None] = mapped_column(sa.UnicodeText, nullable=True)
    missing_points: Mapped[str | None] = mapped_column(sa.UnicodeText, nullable=True)
    incorrect_points: Mapped[str | None] = mapped_column(sa.UnicodeText, nullable=True)
    communication_issues: Mapped[str | None] = mapped_column(sa.UnicodeText, nullable=True)
    qa_comment: Mapped[str | None] = mapped_column(sa.UnicodeText, nullable=True)
    recommendation: Mapped[str | None] = mapped_column(sa.UnicodeText, nullable=True)
    raw_issue_topic: Mapped[str | None] = mapped_column(sa.Unicode(200), nullable=True)
    llm_model: Mapped[str | None] = mapped_column(sa.Unicode(50), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DATETIME2, server_default=sa.text("SYSDATETIME()"), nullable=False
    )
    updated_at: Mapped[datetime | None] = mapped_column(DATETIME2, nullable=True)
    organization_name: Mapped[str | None] = mapped_column(sa.Unicode(100), nullable=True)
    topic_confidence: Mapped[Decimal | None] = mapped_column(sa.DECIMAL(4, 3), nullable=True)
    technical_accuracy_score: Mapped[Decimal | None] = mapped_column(Score, nullable=True)
    troubleshooting_approach_score: Mapped[Decimal | None] = mapped_column(Score, nullable=True)
    completeness_score: Mapped[Decimal | None] = mapped_column(Score, nullable=True)
    case_ownership_score: Mapped[Decimal | None] = mapped_column(Score, nullable=True)
    technical_quality_score: Mapped[Decimal | None] = mapped_column(Score, nullable=True)
    communication_quality_score: Mapped[Decimal | None] = mapped_column(Score, nullable=True)


    topic: Mapped[CanonicalTopic | None] = relationship(lazy="raise")
    ticket: Mapped[TicketSlaCache | None] = relationship(lazy="raise")
    prompt_blocks: Mapped[list[PromptBlock]] = relationship(
        secondary="qa_evaluation_prompt_block",
        order_by=PromptBlock.prompt_block_id,
        lazy="raise",
        viewonly=True,  # рядки звʼязку пише QaEvaluationPromptBlock
    )


class QaEvaluationPromptBlock(Base):
    """Звʼязок M:N між оцінками та блоками промпту."""

    __tablename__ = "qa_evaluation_prompt_block"
    __table_args__ = (
        sa.PrimaryKeyConstraint("qa_evaluation_prompt_block_id", name="pk_qa_eval_pb"),
    )

    qa_evaluation_prompt_block_id: Mapped[int] = mapped_column(
        sa.Integer, sa.Identity(start=1, increment=1)
    )
    prompt_block_id: Mapped[int] = mapped_column(
        sa.Integer,
        sa.ForeignKey("prompt_block.prompt_block_id", name="fk_qa_eval_pb_block"),
        nullable=False,
    )
    qa_evaluation_id: Mapped[int] = mapped_column(
        sa.Integer,
        sa.ForeignKey("qa_evaluation.qa_evaluation_id", name="fk_qa_eval_pb_eval"),
        nullable=False,
    )


class QaEvaluationCopy(Base):
    """ЛР2: журнал змін overall_score, який заповнює тригер tr_qa_evaluation_copy_score."""

    __tablename__ = "qa_evaluation_copy"

    id: Mapped[int] = mapped_column(sa.Integer, sa.Identity(start=1, increment=1), primary_key=True)
    qa_evaluation_id: Mapped[int] = mapped_column(sa.Integer, nullable=False)
    canonical_topic_id: Mapped[int | None] = mapped_column(sa.Integer, nullable=True)
    ticket_id: Mapped[int | None] = mapped_column(sa.Integer, nullable=True)
    result: Mapped[str | None] = mapped_column(sa.Unicode(20), nullable=True)
    overall_score_old: Mapped[Decimal | None] = mapped_column(Score, nullable=True)
    overall_score_new: Mapped[Decimal | None] = mapped_column(Score, nullable=True)
    raw_issue_topic: Mapped[str | None] = mapped_column(sa.Unicode(200), nullable=True)
    agent_name: Mapped[str | None] = mapped_column(sa.Unicode(50), nullable=True)
    copied_at: Mapped[datetime] = mapped_column(
        DATETIME2, server_default=sa.text("SYSDATETIME()"), nullable=False
    )
