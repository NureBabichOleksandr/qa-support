from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.dialects.mssql import DATETIME2
from sqlalchemy.orm import Mapped, mapped_column

from app.core.models import Base


class CanonicalTopic(Base):
    __tablename__ = "canonical_topics"
    __table_args__ = (sa.UniqueConstraint("topic_id", name="uq_canonical_topics_topic_id"),)

    canonical_topic_id: Mapped[int] = mapped_column(
        sa.Integer, sa.Identity(start=1, increment=1), primary_key=True
    )
    topic_id: Mapped[str] = mapped_column(sa.Unicode(50), nullable=False)
    topic_label: Mapped[str] = mapped_column(sa.Unicode(100), nullable=False)
    meaning: Mapped[str | None] = mapped_column(sa.Unicode(500), nullable=True)
    is_active: Mapped[bool] = mapped_column(sa.Boolean, server_default=sa.text("1"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DATETIME2, server_default=sa.text("SYSDATETIME()"), nullable=False
    )
    updated_at: Mapped[datetime | None] = mapped_column(DATETIME2, nullable=True)
    synonyms: Mapped[str | None] = mapped_column(sa.Unicode(500), nullable=True)
    client_aliases: Mapped[str | None] = mapped_column(sa.Unicode(500), nullable=True)
    related_terms: Mapped[str | None] = mapped_column(sa.Unicode(500), nullable=True)
    embedding: Mapped[bytes | None] = mapped_column(sa.LargeBinary, nullable=True)
